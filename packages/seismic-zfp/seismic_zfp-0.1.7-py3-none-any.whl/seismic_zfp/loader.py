try:
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache
from psutil import virtual_memory
import numpy as np
import zfpy
from .sgzconstants import DISK_BLOCK_BYTES


class SgzLoader(object):
    def __init__(self, file, data_start_bytes, compressed_data_diskblocks, shape_pad, blockshape,
                 chunk_bytes, block_bytes, unit_bytes, rate, preload=False):
        self.file = file
        self.data_start_bytes = data_start_bytes
        self.compressed_data_diskblocks = compressed_data_diskblocks
        self.shape_pad = shape_pad
        self.blockshape = blockshape
        self.chunk_bytes = chunk_bytes
        self.block_bytes = block_bytes
        self.unit_bytes = unit_bytes
        self.rate = rate

        self.compressed_volume = None
        if preload:
            uncompressed_buf_size = self.compressed_data_diskblocks * DISK_BLOCK_BYTES * (32 / self.rate)
            if uncompressed_buf_size > virtual_memory().total:
                msg = "Uncompressed volume is {}MB, machine memory is {}MB, try using 'preload=False'"
                print(msg.format(uncompressed_buf_size//(1024*1024), virtual_memory().total//(1024*1024)))
                raise RuntimeError("Out of memory.  We wish to hold the whole sky,  But we never will.")
            self.load_compressed_volume()

    def load_compressed_volume(self):
        if self.compressed_volume is None:
            self.file.seek(self.data_start_bytes)
            self.compressed_volume = self.file.read(self.compressed_data_diskblocks * self.block_bytes)
        else:
            pass

    def _get_compressed_bytes(self, offset, length_bytes):
        if self.compressed_volume is not None:
            return self.compressed_volume[offset:offset+length_bytes]
        else:
            self.file.seek(self.data_start_bytes + offset, 0)
            return self.file.read(length_bytes)

    def _decompress(self, buffer, shape):
        return zfpy._decompress(bytes(buffer), zfpy.dtype_to_ztype(np.dtype('float32')), shape, rate=self.rate)

    @lru_cache(maxsize=1)
    def read_and_decompress_il_set(self, i):
        il_block_offset = ((self.chunk_bytes * self.shape_pad[1]) // 4) * (i // 4)
        buffer = self._get_compressed_bytes(il_block_offset, self.chunk_bytes * self.shape_pad[1])
        return self._decompress(buffer, (self.blockshape[0], self.shape_pad[1], self.shape_pad[2]))

    @lru_cache(maxsize=1)
    def read_and_decompress_xl_set(self, x):
        xl_first_chunk_offset = x // 4 * self.chunk_bytes
        xl_chunk_increment = self.chunk_bytes * self.shape_pad[1] // 4
        buffer = bytearray(self.chunk_bytes * self.shape_pad[0] // 4)
        for chunk_num in range(self.shape_pad[0] // 4):
            part = self._get_compressed_bytes(xl_first_chunk_offset + chunk_num * xl_chunk_increment, self.chunk_bytes)
            buffer[chunk_num * self.chunk_bytes:(chunk_num + 1) * self.chunk_bytes] = part
        return self._decompress(buffer, (self.shape_pad[0], self.blockshape[1], self.shape_pad[2]))

    @lru_cache(maxsize=1)
    def read_and_decompress_zslice_set(self, blocks_per_dim, zslice_first_block_offset, zslice_id):
        zslice_unit_in_block = (zslice_id % self.blockshape[2]) // 4
        buffer = bytearray(self.unit_bytes * (blocks_per_dim[0]) * (blocks_per_dim[1]))
        for block_num in range((blocks_per_dim[0]) * (blocks_per_dim[1])):
            part = self._get_compressed_bytes(zslice_first_block_offset * self.block_bytes
                                              + zslice_unit_in_block * self.unit_bytes
                                              + block_num * self.chunk_bytes, self.unit_bytes)
            buffer[block_num * self.unit_bytes:(block_num + 1) * self.unit_bytes] = part
        return self._decompress(buffer, (self.shape_pad[0], self.shape_pad[1], 4))

    @lru_cache(maxsize=1)
    def read_and_decompress_zslice_set_adv(self, blocks_per_dim, zslice_first_block_offset):
        sub_block_size_bytes = ((4 * 4 * self.blockshape[1]) * self.rate) // 8
        buffer = bytearray(self.block_bytes * blocks_per_dim[0] * blocks_per_dim[1])
        for block_i in range(blocks_per_dim[0]):
            for block_x in range(blocks_per_dim[1]):
                block_num = block_i * (blocks_per_dim[1]) + block_x
                temp_buf = self._get_compressed_bytes(zslice_first_block_offset * self.block_bytes
                                                      + block_num * (self.block_bytes * (blocks_per_dim[2])),
                                                      self.block_bytes)
                for sub_block_num in range(self.blockshape[0] // 4):
                    buf_start = block_i * self.block_bytes * (
                        blocks_per_dim[1]) + block_x * sub_block_size_bytes + sub_block_num * (
                                            (self.shape_pad[1] * 4 * 4 * self.rate) // 8)
                    buffer[buf_start:buf_start + sub_block_size_bytes] = \
                        temp_buf[sub_block_num * sub_block_size_bytes:(sub_block_num + 1) * sub_block_size_bytes]
        return self._decompress(buffer, (self.shape_pad[0], self.shape_pad[1], 4))

    @lru_cache(maxsize=1)
    def read_and_decompress_chunk_range(self, max_il, max_xl, max_z, min_il, min_xl, min_z):
        z_units = (max_z + 3) // 4 - min_z // 4
        xl_units = (max_xl + 3) // 4 - min_xl // 4
        il_units = (max_il + 3) // 4 - min_il // 4

        buffer = bytearray(z_units * xl_units * il_units * self.unit_bytes)
        read_length = self.unit_bytes * z_units
        for i in range(il_units):
            for x in range(xl_units):
                # No need to loop over z... it's contiguous, so do it in one file read
                bytes_start = self.unit_bytes * (
                                (i + (min_il // 4)) * (self.shape_pad[1] // 4) * (self.shape_pad[2] // 4) +
                                (x + (min_xl // 4)) * (self.shape_pad[2] // 4) +
                                (min_z // 4))
                buf_start = (i * xl_units * z_units + x * z_units) * self.unit_bytes
                buf_end = buf_start + read_length
                part = self._get_compressed_bytes(bytes_start, read_length)
                buffer[buf_start:buf_end] = part
        return self._decompress(buffer, (il_units * 4, xl_units * 4, z_units * 4))

    @lru_cache(maxsize=1)
    def read_unshuffle_and_decompress_chunk_range(self, max_il, max_xl, max_z, min_il, min_xl, min_z):
        z_blocks = (max_z + self.blockshape[2]) // self.blockshape[2] - min_z // self.blockshape[2]
        xl_blocks = (max_xl + self.blockshape[1]) // self.blockshape[1] - min_xl // self.blockshape[1]
        il_blocks = (max_il + self.blockshape[0]) // self.blockshape[0] - min_il // self.blockshape[0]
        decompressed = np.zeros((il_blocks * self.blockshape[0],
                                 xl_blocks * self.blockshape[1],
                                 z_blocks * self.blockshape[2]), dtype=np.float32)
        for i in range(il_blocks):
            for x in range(xl_blocks):
                for z in range(z_blocks):
                    bytes_start = self.block_bytes * (
                            (i + (min_il // self.blockshape[0])) * (self.shape_pad[1] // self.blockshape[1]) * (
                                self.shape_pad[2] // self.blockshape[2]) +
                            (x + (min_xl // self.blockshape[1])) * (self.shape_pad[2] // self.blockshape[2]) +
                            (z + (min_z // self.blockshape[2])))
                    buffer = self._get_compressed_bytes(bytes_start, self.block_bytes)
                    decompressed_part = self._decompress(buffer,
                                                         (self.blockshape[0], self.blockshape[1], self.blockshape[2]))
                    decompressed[i * self.blockshape[0]:(i + 1) * self.blockshape[0],
                    x * self.blockshape[1]:(x + 1) * self.blockshape[1],
                    z * self.blockshape[2]:(z + 1) * self.blockshape[2]] = decompressed_part
        return decompressed
