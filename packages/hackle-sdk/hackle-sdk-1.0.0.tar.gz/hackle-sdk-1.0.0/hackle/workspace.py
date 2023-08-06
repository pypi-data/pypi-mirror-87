import json

from . import entities


class Workspace(object):
    def __init__(self, data, logger):
        self.variation_id_map = None
        json_data = json.loads(data)
        self.logger = logger
        self.logger.debug('data : {}'.format(json_data))

        self.workspace = json_data.get('workspace')
        self.experiments = json_data.get('experiments', [])
        self.completedExperiments = json_data.get('completedExperiments', [])
        self.buckets = json_data.get('buckets', [])
        self.events = json_data.get('events', [])

        self.experiment_key_map = {}
        self.completed_experiment_key_map = {}
        self.bucket_id_map = {}
        self.event_key_map = {}

        for bucket in self.buckets:
            slots = []
            for slot in bucket['slots']:
                slots.append(entities.Slot(slot['startInclusive'], slot['endExclusive'], slot['variationId']))
            self.bucket_id_map[bucket['id']] = entities.Bucket(bucket['seed'], bucket['slotSize'], slots)

        for event in self.events:
            self.event_key_map[str(event['key'])] = entities.Event(event['id'], event['key'])

        for experiment in self.experiments:
            variations = {}
            for variation in experiment['variations']:
                variations[variation['id']] = entities.Variation(variation['id'], variation['key'],
                                                                 variation['status'] == 'DROPPED')

                self.experiment_key_map[experiment['key']] = entities.RunningExperiment(experiment['id'],
                                                                                        experiment['key'],
                                                                                        self.bucket_id_map[
                                                                                            experiment[
                                                                                                'bucketId']],
                                                                                        variations,
                                                                                        experiment['execution']
                                                                                        )

        for completedExperiment in self.completedExperiments:
            self.completed_experiment_key_map[completedExperiment['experimentKey']] = entities.CompletedExperiment(
                completedExperiment['experimentId'],
                completedExperiment['experimentKey'],
                completedExperiment['winnerVariationKey']
            )
            self.experiment_key_map[completedExperiment['experimentKey']] = entities.CompletedExperiment(
                completedExperiment['experimentId'],
                completedExperiment['experimentKey'],
                completedExperiment['winnerVariationKey']
            )

    @staticmethod
    def _generate_key_map(entity_list, key, entity_class):
        key_map = {}
        for obj in entity_list:
            print(type(obj))
            key_map[obj[key]] = entity_class(**obj)

        return key_map

    def get_experiment_from_key(self, experiment_key):
        experiment = self.experiment_key_map.get(experiment_key)
        if experiment:
            return experiment

        self.logger.error('Experiment Key %s is not defined.' % experiment_key)

        return None

    def get_completed_experiment_from_key(self, experiment_key):
        completed_experiment = self.completed_experiment_key_map.get(experiment_key)

        if completed_experiment:
            return completed_experiment

        return None

    def get_event(self, event_key):
        event = self.event_key_map.get(event_key)

        if event:
            return event
        else:
            return entities.Event(0, event_key)
