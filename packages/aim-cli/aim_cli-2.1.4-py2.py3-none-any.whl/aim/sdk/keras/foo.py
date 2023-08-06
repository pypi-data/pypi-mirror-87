from aim.engine.utils import get_module


keras = get_module('keras') or get_module('tf.keras')


class TrackCallback(keras.callbacks.Callback):
    def _collect_learning_rate(self, logs):
        pass
        # lr_schedule = getattr(self.model.optimizer, 'lr', None)
        # if isinstance(lr_schedule, learning_rate_schedule.LearningRateSchedule):
        #     logs['learning_rate'] = lr_schedule(self.model.optimizer.iterations)
        # return logs

    def _log_epoch_metrics(self, epoch, logs):
        if not logs:
            return

        train_logs = {k: v for k, v in logs.items() if not k.startswith('val_')}
        val_logs = {k: v for k, v in logs.items() if k.startswith('val_')}
        # train_logs = self._collect_learning_rate(train_logs)

        print(train_logs, val_logs)
        #
        # with summary_ops_v2.always_record_summaries():
        #     if train_logs:
        #         with self._train_writer.as_default():
        #             for name, value in train_logs.items():
        #                 summary_ops_v2.scalar('epoch_' + name, value,
        #                                       step=epoch)
        #     if val_logs:
        #         with self._val_writer.as_default():
        #             for name, value in val_logs.items():
        #                 name = name[4:]  # Remove 'val_' prefix.
        #                 summary_ops_v2.scalar('epoch_' + name, value,
        #                                       step=epoch)

    def on_epoch_end(self, epoch, logs=None):
        """Runs metrics and histogram summaries at epoch end."""
        self._log_epoch_metrics(epoch, logs)
