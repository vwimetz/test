import torch


# Define the RoomPopulationModel class
class RoomPopulationModel(torch.nn.Module):
    def __init__(self, input_size=3408, output_size=1608):
        super(RoomPopulationModel, self).__init__()
        self.seq = torch.nn.Sequential(
            torch.nn.Linear(input_size, input_size * 4, dtype=torch.float64),
            torch.nn.ReLU(),
            torch.nn.Linear(input_size * 4, input_size, dtype=torch.float64),
            torch.nn.ReLU(),
            torch.nn.Linear(input_size, output_size, dtype=torch.float64),
        )

    def forward(self, x):
        return self.seq(x)


# Load the model
model = RoomPopulationModel()
model.load_state_dict(torch.load('model.pt'))

# Ensure the model is in evaluation mode
model.eval()

# Create an input tensor that matches the input size your model expects
# Replace this with the appropriate code for your specific model
input_tensor = torch.randn(1, 3408)

# Pass the input tensor through the model
output = model(input_tensor)

# Print the output
print(output)
