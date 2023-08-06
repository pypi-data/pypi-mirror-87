

class Mask(nn.Module):
    def __init__(self, *dims):
        super(Mask, self).__init__()
        self.dimension = torch.Size([dims])
        self.weight = self.get_new_mask_weight()
        self.weight.data.uniform_(0.88, 0.99)

    def forward(self, x):
        x_dims = x.s
        x_1d = torch.flatten(x)
        # To-Do
        # Flatt to 2D
        # MatMul
        # Unflat
        return self.weight.mul(x)

    def get_new_mask_weight(self, requires_grad=True):
        return torch.nn.Parameter(data=torch.Tensor(self.dimension), requires_grad=requires_grad)


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.Mask = Mask(100)

    def forward(self, x):
        x = Mask(x)
        return x

# def AutoRetroActionEncoder(input_dim, output_dim=0, scale=1, load=0):
#     if output_dim == 0:
#         # Calculate the correct scale for the parameters

#         scaled = 1
#         output_dim = scaled

#     return nn.Sequential(nn.ConvTranspose2d())




# Recall that a variable y satisfies exponential growth if it satisfies the differential equation y ' = k * y (where k > 0). The solution to this differential equation is y = C * e^( k * t ), where C represents the initial value of y at time t = 0. Typically the value of k is found from knowing the value of y at some other time t. 
# Use this information to solve the following: A bacteria population starts with 4 million bacteria and triples every 30 minutes. How many bacteria are present after 45 minutes? 

# C = 4e6;
# k = log(3)/30;
# t = 45;
# y = C*exp(k*t);

