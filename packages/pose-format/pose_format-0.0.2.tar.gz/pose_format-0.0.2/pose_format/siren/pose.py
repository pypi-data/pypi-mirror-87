import numpy as np
import torch
from numpy import ma
from torch.utils.data import DataLoader, Dataset

from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
from pose_format.utils.siren import Siren


class PoseFitting(Dataset):
    def __init__(self, pose):
        super().__init__()

        # TODO add confidence
        self.poses = torch.tensor([pose.flatten() for pose in np.array(p.body.data.data)], dtype=torch.float32)
        self.confidence = torch.tensor([np.stack([c, c], axis=-1).flatten() for c in np.array(p.body.confidence)],
                                       dtype=torch.float32)
        self.coords = torch.tensor([[i] for i in range(len(self.poses))], dtype=torch.float32)

    def __len__(self):
        return 1

    def __getitem__(self, idx):
        if idx > 0: raise IndexError

        return self.coords, self.poses, self.confidence


buffer = open("/home/nlp/amit/PhD/PoseFormat/sample-data/1.pose", "rb").read()
# buffer = open("/home/nlp/amit/PhD/SpeakerDetection/dgs-korpus/poses/76fb03008e26466f472ef3989232e1cf.pose", "rb").read()
p = Pose.read(buffer)

info = p.header.normalization_info(
    p1=("pose_keypoints_2d", "RShoulder"),
    p2=("pose_keypoints_2d", "LShoulder")
)
p.body.data = p.body.data
p.body.confidence = p.body.confidence
p = p.normalize(info, scale_factor=1)
p.body.zero_filled()

dataset = PoseFitting(p)
dataloader = DataLoader(dataset, batch_size=1, pin_memory=True, num_workers=0)

siren = Siren(in_features=1, out_features=137 * 2, hidden_features=512,
              hidden_layers=4, outermost_linear=True)
siren.cuda()


#
#
#


def train_siren(net, dataloader, total_steps=5000, steps_til_summary=50):
    optim = torch.optim.Adam(lr=1e-5, params=net.parameters())

    model_input, ground_truth, confidence = next(iter(dataloader))
    model_input, ground_truth, confidence = model_input.cuda(), ground_truth.cuda(), confidence.cuda()

    for step in range(total_steps):
        model_output, coords = net(model_input)

        sq_error = (model_output - ground_truth) ** 2
        loss = (sq_error * confidence).mean()

        if not step % steps_til_summary:
            print("Step %d, Total loss %0.6f" % (step, loss))

        optim.zero_grad()
        loss.backward()
        optim.step()

    output = model_output.cpu().detach().numpy()
    pose_data = output.reshape((output.shape[1], 1, 137, 2))

    return pose_data


p.body.confidence = np.ones_like(p.body.confidence)
p.body.data = ma.array(train_siren(siren, dataloader))

p.normalize(info, scale_factor=500)
p.focus()

v = PoseVisualizer(p)
v.save_video("test2.mp4", v.draw())
