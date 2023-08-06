from azureml.studio.internal.error import ErrorMapping, InvalidDatasetError, ModuleOutOfMemoryError


def raise_error(e, for_training=True):
    if isinstance(e, RuntimeError):
        if "Sizes of tensors must match" in str(e.args):
            ErrorMapping.rethrow(
                e,
                InvalidDatasetError(
                    dataset1=f"{'Training' if for_training else 'Validation'} dataset",
                    reason=f"Got exception when {'training' if for_training else 'evaluating'} per epoch: "
                    f"{ErrorMapping.get_exception_message(e)}",
                    troubleshoot_hint="Please make sure all images the same size in dataset, referring to "
                                      "https://docs.microsoft.com/en-us/azure/machine-learning/"
                                      "algorithm-module-reference/init-image-transformation."))
        if any(err_msg.lower() in str(e.args).lower() for err_msg in ["CUDA out of memory", "can't allocate memory"]):
            ErrorMapping.rethrow(
                e,
                ModuleOutOfMemoryError(f"Cannot allocate more memory because {ErrorMapping.get_exception_message(e)}. "
                                       f"Please reduce hyper-parameter 'Batch size', or upgrade VM Sku."))

    raise e


class AverageMeter(object):
    """Computes and stores the average and current value
    Copied from: https://github.com/pytorch/examples/blob/master/imagenet/main.py
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
