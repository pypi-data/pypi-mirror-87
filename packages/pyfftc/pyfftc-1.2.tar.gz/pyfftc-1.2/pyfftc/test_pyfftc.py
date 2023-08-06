import unittest
import torch
import pyfftc

DTYPE = torch.complex64
EPS = torch.finfo(DTYPE).eps * 10

class test_util(unittest.TestCase):
          
    def test_fftshift_even(self,):
        Np = 10
        x = torch.linspace(-Np//2, Np//2 - 1, Np)
        out = pyfftc.ifftshift(pyfftc.fftshift(x)) - x
        self.assertTrue(torch.abs(torch.sum(out)) < EPS)
        
    def test_fftshift_odd(self, ):
        Np = 11
        x = torch.linspace(-Np//2 + 1, Np//2 , Np)
        out = pyfftc.ifftshift(pyfftc.fftshift(x)) - x
        self.assertTrue(torch.abs(torch.sum(out)) < EPS)
        
    def test_fft_even(self,):
        Np = [100, ]
        x = torch.rand((*Np), dtype=DTYPE)
        out = pyfftc.ifftc(pyfftc.fftc(x)) - x
        bool_out = (torch.abs(out) < EPS).byte().all()
        self.assertTrue(bool_out)
                
    def test_fft_odd(self,):
        Np = [101, ]
        x = torch.rand((*Np), dtype=DTYPE)
        out = pyfftc.ifftc(pyfftc.fftc(x)) - x
        bool_out = (torch.abs(out) < EPS).byte().all()
        self.assertTrue(bool_out)