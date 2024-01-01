import torchvision.transforms as transforms

# numpy转tensor
def numpyToTensor(numpy):
    transf = transforms.ToTensor()
    tensor = transf(numpy).permute(1, 2, 0).unsqueeze(0)
    return tensor

# tensor转numpy
def tensorToNumpy(tensor):
    return tensor.squeeze(0).numpy()
