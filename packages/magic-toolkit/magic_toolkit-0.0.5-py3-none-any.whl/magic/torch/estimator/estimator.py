from magic.common import LOG_INFO
import torch
from torch import nn
from torchsummary import summary
from torch.utils.tensorboard import SummaryWriter

class Estimator:
    def __init__(self, model: nn.Module, pre_trained, inputs_size):
        """
        :param model:
        :param pre_trained:
        :param inputs_size: list of size, [[C, H, W], [C, H, W], ...]
        """
        # pre-defined member data
        self.summary_writer = SummaryWriter()  # tensorboard
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        # member data passed in
        self.model = model
        self.pre_trained = pre_trained
        self.inputs_size = inputs_size

    def set_train_mode(self):
        if not self.model.training:
            self.model.train()
        else:
            return True

    def set_eval_mode(self):
        if self.model.training:
            self.model.eval()
        else:
            return True

    def summary(self):
        """
        support multiple inputs to the network
        :param inputs_size, list of size, don't contain batch size: [[C, H, W], [C, H, W], ...]
        """
        inputs_size = [tuple(size) for size in self.inputs_size]  # need tuple type

        self.model.to(self.device)

        # add graph to tensorboard
        batch = 1
        dummy_inputs = tuple([torch.randn(batch, *size).to(self.device) for size in inputs_size])
        torch_model = self.model.module if hasattr(self.model, "module") else self.model
        self.summary_writer.add_graph(torch_model, dummy_inputs)
        self.summary_writer.flush()

        LOG_INFO("model summary .. ")
        summary(torch_model, inputs_size, batch_size=batch, device=self.device.type)

    def load(self, strict=False):
        """
        Partially loading a model or loading a partial model are common scenarios
        when transfer learning or training a new complex model. Leveraging trained parameters,
        even if only a few are usable, will help to warmstart the training process and
        hopefully help your model converge much faster than training from scratch.
        you can set the strict argument to False in the load_state_dict() function to ignore non-matching keys
        """
        pre_trained = self.pre_trained

        LOG_INFO("loading pre_trained model ... ")
        self.model.to(self.device)
        checkpoint = torch.load(pre_trained, map_location=self.device)
        if hasattr(self.model, "module"):
            self.model.module.load_state_dict(checkpoint, strict=strict)
        else:
            self.model.load_state_dict(checkpoint, strict=strict)

    def save(self, model_path=None):
        """ save model """
        if model_path is None:
            model_path = self.pre_trained

        """
        torch.nn.DataParallel is a model wrapper that enables parallel GPU utilization.
        To save a DataParallel model generically, save the model.module.state_dict(). 
        This way, you have the flexibility to load the model any way you want to any device you want.
        """

        if hasattr(self.model, "module"):
            if len(self.model.module.state_dict()) == 0:
                raise RuntimeError("model is empty")
            torch.save(self.model.module.state_dict(), model_path)
        else:
            if len(self.model.state_dict()) == 0:
                raise RuntimeError("model is empty")
            torch.save(self.model.state_dict(), model_path)
        LOG_INFO("saved to {}".format(model_path))

    def export_onnx(self, onnx_path, opset_version=8, batch=1, verbose=False):
        """
        Exporting a model in PyTorch works via tracing or scripting.
        To export a model, we call the torch.onnx.export() function.
        This will execute the model, recording a trace of what operators are used to compute the outputs.
        Because export runs the model, we need to provide an input tensor x.
        The values in this can be random as long as it is the right type and size.
        :param onnx_path
        :param opset_version: onnx version
        :param batch: for onnx batch
        :param input_names: can ignore
        :param output_names: can ignore
        """

        import onnx
        from onnxsim import simplify

        # Export the model
        self.model.to(self.device)  # set the model to inference mode
        self.set_eval_mode()

        dummy_inputs = tuple([torch.randn(batch, *size).to(self.device) for size in self.inputs_size])

        torch_model = self.model.module if hasattr(self.model, "module") else self.model

        torch.onnx.export(torch_model,  # model being run
                          dummy_inputs,  # model input (or a tuple for multiple inputs)
                          onnx_path,  # where to save the model (can be a file or file-like object)
                          export_params=True,  # store the trained parameter weights inside the model file
                          opset_version=opset_version,  # the ONNX version to export the model to
                          do_constant_folding=True,  # whether to execute constant folding for optimization
                          input_names=[],  # the model's input names
                          output_names=[],  # the model's output names
                          verbose=verbose
                          )

        # load your predefined ONNX model
        onnx_model = onnx.load(onnx_path)
        onnx_model, check = simplify(onnx_model)
        assert check, "Simplified ONNX model could not be validated"
        onnx.save(onnx_model, onnx_path)
        LOG_INFO("onnx saved to: {}".format(onnx_path))
