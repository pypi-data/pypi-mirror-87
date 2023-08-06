from . import decider
from . import exceptions as hackle_exceptions
from . import logger as _logging
from .commons import validator, enums
from .event import event_processor, event as event_entity
from .event.event_dispatcher import EventDispatcher
from .workspace_fetcher import WorkspaceFetcher


def __singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


@__singleton
class Client(object):
    def __init__(
            self,
            sdk_key=None,
            logger=None
    ):
        if sdk_key is None:
            raise hackle_exceptions.RequiredParameterException('sdk_key must not be empty')

        self.event_dispatcher = EventDispatcher()
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())
        self.event_processor = event_processor.BatchEventProcessor(sdk_key, self.event_dispatcher, self.logger)
        self.decider = decider.Decider(self.logger)
        self.workspace_fetcher = WorkspaceFetcher(sdk_key, logger=self.logger)

    def close(self):
        self.workspace_fetcher.stop()
        self.event_processor.stop()

    def __exit__(self):
        self.close()

    def variation(self, experiment_key, user, default_variation='A'):
        """
        Decide the variation to expose to the user for experiment.

        This method return the "A" if:
            - The experiment key is invalid
            - The experiment has not started yet
            - The user is not allocated to the experiment
            - The decided variation has been dropped

        :param int experiment_key: the unique key of the experiment.
        :param hackle.model.User user: the identifier of your customer (e.g. user_email, account_id, etc.) MUST NOT be
         null.
        :param str default_variation: the default variation of the experiment. MUST NOT be null.
        :return: the decided variation for the user, or the default variation.
        """
        if not validator.is_non_zero_and_empty_int(experiment_key):
            self.logger.error('Experiment Key Is Not Empty : {}'.format(experiment_key))
            return default_variation

        if not validator.is_valid_user(user):
            self.logger.error('User is not valid. user\'s type must be hackle.model.User and user.id\'s type must be '
                              'string_types : {}'.format(user))
            return default_variation

        config = self.workspace_fetcher.get_config()
        if not config:
            self.logger.error('Invalid Workspace. Hackle instance is not valid. {}'.format('variation'))
            return default_variation

        experiment = config.get_experiment_from_key(experiment_key)

        if not experiment:
            self.logger.info('Experiment Key "%s" is invalid. Not Allocated.' % experiment_key)
            return default_variation

        decision = self.decider.decide(experiment, user)
        if not decision:
            return default_variation

        if decision.type == enums.DecisionType.FORCED:
            return decision.variation
        elif decision.type == enums.DecisionType.NATURAL:
            self.event_processor.process(
                event_entity.ExposureEvent(user, decision.experiment.id, decision.experiment.key, decision.variation.id,
                                           decision.variation.key))
            return decision.variation.key
        return default_variation

    def track(self, event, user):
        """
        Records the event performed by the user with additional numeric value.

        :param hackle.model.Event event: the unique key of the event. MUST NOT be null.
        :param user: the identifier of user that performed the event. MUST NOT be null.
        :return:
        """
        if not validator.is_valid_event(event):
            self.logger.error('Event is not valid. Event must be hackle.model.event and event.id\'s type must be '
                              'string_types. value\'s type must be numeric. '
                              ': {}'.format(event))
            return

        if not validator.is_valid_user(user):
            self.logger.error('User is not valid. user\'s type must be hackle.model.User and user.id\'s type must be '
                              'string_types : {}'.format(user))
            return

        config = self.workspace_fetcher.get_config()
        if not config:
            self.logger.error('Invalid Workspace. Hackle instance is not valid. {}'.format('event'))
            return

        event_type = config.get_event(event.key)
        self.event_processor.process(
            event_entity.TrackEvent(user, event_type, event)
        )

        return

    def user(self, id, properties=None):
        if not validator.is_non_empty_string(id):
            self.logger.error('id Is Not Empty : {}'.format(id))
            return

        if properties and validator.is_valid_user(properties):
            self.logger.error('properties is not valid : {}'.format(id))
            return

        # TODO
        return
