import tensorrt as trt
# import pycuda.driver as cuda
# import pycuda.autoinit

def onnx_convert(onnx_path,
                 trt_path,
                 max_batch_size=1,
                 fp16=0,
                 int8=0,
                 calibrator=None,
                 verbose=0,
                 network_ext_fn=None):
    """
    onnx -> trt
    support fp32, fp16, int8
    :param onnx_path: onnx model path
    :param trt_path: for save engine
    :param max_batch_size: fixed batch not dynamic batch
    :param fp16: turn on fp16
    :param int8: turn on int8
    :param calibrator: int8 calibrator
    :param verbose: whether to print tensorrt log of processing.
    :param network_ext_fn: extend network by tensorrt api
    """

    # get tensorrt version
    trt_version = trt.__version__
    print("tensorrt version:", trt_version)
    # cuda_version = cuda.get_version()
    # print("cuda version:", cuda_version)

    # instantiate Logger
    severity = trt.Logger.VERBOSE if verbose else trt.Logger.WARNING
    TRT_LOGGER = trt.Logger(severity)

    #builder properties
    builder = trt.Builder(TRT_LOGGER)
    builder.max_workspace_size = 1 << 30  # 1GB
    builder.max_batch_size = max_batch_size

    if fp16:
        if builder.platform_has_fast_fp16:
            builder.fp16_mode = True
        else:
            raise RuntimeError("不支持fp16")

    if int8:
        if builder.platform_has_fast_int8:
            builder.int8_mode = True
            builder.int8_calibrator = calibrator
        else:
            raise RuntimeError("不支持int8")

    # create network
    network = None
    if trt_version[0] in ["5", "6"]:
        network = builder.create_network()
    if trt_version[0] in ["7"]:
        EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
        network = builder.create_network(EXPLICIT_BATCH)

    # load onnx to parse
    parser = trt.OnnxParser(network, TRT_LOGGER)
    with open(onnx_path, 'rb') as model:
        try:
            bState = parser.parse(model.read())
        except Exception as e:
            print(e)
        print('Completed parsing of ONNX file:', bState)

    if network_ext_fn:
        network_ext_fn(network)

    print('Building, this may take a while...')

    engine = builder.build_cuda_engine(network)
    with open(trt_path, "wb") as f:
        f.write(engine.serialize())
        print('Saved engin in {}'.format(trt_path))

    print("engine.max_batch_size={}".format(engine.max_batch_size))
    for i in range(engine.num_bindings):
        binding_type = "input_node:" if engine.binding_is_input(i) else "output_node:"
        binding_name = engine.get_binding_name(i)
        binding_shape = engine.get_binding_shape(i)
        print(binding_type, binding_name, binding_shape)
