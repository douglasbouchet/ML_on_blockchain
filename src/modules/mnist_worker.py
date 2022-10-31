from src.modules.worker import Worker

# import torchvision
# import torchvision.datasets as datasets


class MnsitWorker(Worker):
    def __init__(self, address, private_key):
        super(MnsitWorker, self).__init__(address, private_key)
        self.model = None
        # self.mnist_trainset = datasets.MNIST(
        #     root="/home/user/ml_on_blockchain/resources/mnist_data",
        #     train=True,
        #     download=True,
        #     transform=None,
        # )
        # self.mnist_testset = datasets.MNIST(
        #     root="/home/user/ml_on_blockchain/resources/mnist_data",
        #     train=False,
        #     download=True,
        #     transform=None,
        # )

    # def load_model(self):
    #     self.model = load_model("mnist.h5")

    # def handle(self, data):
    #    if self.model is None:
    #        self.load_model()
    #    x = np.array(data["x"])
    #    y = self.model.predict(x)
    #    return y.tolist()
