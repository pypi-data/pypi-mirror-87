import torch
import torch.fft

def roll(x, N):
    return torch.cat((x[-N:,...], x[:-N,...]), dim=0)

def fftshift1(x):
    N = x.shape
    if N[0] % 2 == 0:
        x = roll(x, N[0]//2)
    else:
        x = roll(x, N[0]//2 + 1)
    return x

def ifftshift1(x):
    N = x.shape
    if N[0] % 2 == 0:
        x = roll(x, N[0]//2)
    else:
        x = roll(x, N[0]//2)
    return x

def fftshift(x, batch=False):
	if batch is False:
		start_idx = 0
	else:
		start_idx = 1

	for ii in range(start_idx, len(x.shape)):
		x = torch.transpose(fftshift1(torch.transpose(x, ii, 0)), ii, 0)
	return x


def ifftshift(x, batch=False):
	if batch is False:
		start_idx = 0
	else:
		start_idx = 1

	for ii in range(start_idx, len(x.shape)):
		x = torch.transpose(ifftshift1(torch.transpose(x, ii, 0)), ii, 0)
	return x


def fftc(x):
    return fftshift(torch.fft.fftn(ifftshift(x)))

def ifftc(x):
    return fftshift(torch.fft.ifftn(ifftshift(x)))