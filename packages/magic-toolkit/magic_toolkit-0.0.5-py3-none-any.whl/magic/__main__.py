import argparse

def main():
    parser = argparse.ArgumentParser()
    # list something
    parser.add_argument('--list', default='', metavar='', help='.trt')
    # get config template
    parser.add_argument('--config', default='', metavar='', help='get config template: pytorch, tensorflow')
    # onnx to trt
    parser.add_argument("--onnx", default='', metavar='', help="onnx path")
    parser.add_argument('--batch', default=1, type=int, metavar='', help="tensorrt max batch，default=1")
    parser.add_argument("--fp16", default=0, type=int, metavar='', help="default=0")

    args = parser.parse_args()

    # list trt engine info
    if args.list.endswith(".trt"):
        from magic.tensorrt.trt_infer import TrtSession
        sess = TrtSession()
        sess.load_engine(args.list)

    # get config template
    if len(args.config):
        from magic.common import get_config_template
        get_config_template(args.config)

    # onnx to trt
    if len(args.onnx):
        from magic.tensorrt.onnx2trt import onnx_convert
        assert args.onnx.endswith(".onnx"), "need .onnx"
        onnx_convert(args.onnx, args.onnx.split('.')[0] + ".trt", args.batch, args.fp16, verbose=1)

if __name__ == '__main__':
    main()