"""Test the collective allreduice API on a distributed Ray cluster."""
import pytest
import ray
from ray.util.collective.types import ReduceOp

import numpy as np
import torch

from ray.util.collective.types import Backend
from ray.util.collective.tests.cpu_util import create_collective_workers


@pytest.mark.parametrize("backend", [Backend.GLOO])
@pytest.mark.parametrize("group_name", ["default", "test", "123?34!"])
@pytest.mark.parametrize("world_size", [5, 6, 7, 8])
def test_allreduce_different_name(ray_start_distributed_2_nodes, group_name,
                                  world_size, backend):
    actors, _ = create_collective_workers(
        num_workers=world_size, group_name=group_name, backend=backend)
    results = ray.get([a.do_allreduce.remote(group_name) for a in actors])
    assert (results[0] == np.ones((10, ), dtype=np.float32) * world_size).all()
    assert (results[1] == np.ones((10, ), dtype=np.float32) * world_size).all()


@pytest.mark.parametrize("backend", [Backend.GLOO])
@pytest.mark.parametrize("array_size", [2, 2**5, 2**10, 2**15, 2**20])
def test_allreduce_different_array_size(ray_start_distributed_2_nodes,
                                        array_size, backend):
    world_size = 8
    actors, _ = create_collective_workers(world_size, backend=backend)
    ray.wait([
        a.set_buffer.remote(np.ones(array_size, dtype=np.float32))
        for a in actors
    ])
    results = ray.get([a.do_allreduce.remote() for a in actors])
    assert (results[0] == np.ones(
        (array_size, ), dtype=np.float32) * world_size).all()
    assert (results[1] == np.ones(
        (array_size, ), dtype=np.float32) * world_size).all()


@pytest.mark.parametrize("backend", [Backend.GLOO])
def test_allreduce_destroy(ray_start_distributed_2_nodes,
                           backend,
                           group_name="default"):
    world_size = 8
    actors, _ = create_collective_workers(world_size, backend=backend)

    results = ray.get([a.do_allreduce.remote() for a in actors])
    assert (results[0] == np.ones((10, ), dtype=np.float32) * world_size).all()
    assert (results[1] == np.ones((10, ), dtype=np.float32) * world_size).all()

    # destroy the group and try do work, should fail
    ray.get([a.destroy_group.remote() for a in actors])
    with pytest.raises(RuntimeError):
        results = ray.get([a.do_allreduce.remote() for a in actors])

    # reinit the same group and all reduce
    ray.get([
        actor.init_group.remote(world_size, i, backend, group_name)
        for i, actor in enumerate(actors)
    ])
    results = ray.get([a.do_allreduce.remote() for a in actors])
    assert (results[0] == np.ones(
        (10, ), dtype=np.float32) * world_size * world_size).all()
    assert (results[1] == np.ones(
        (10, ), dtype=np.float32) * world_size * world_size).all()


@pytest.mark.parametrize("backend", [Backend.GLOO])
def test_allreduce_multiple_group(ray_start_distributed_2_nodes,
                                  backend,
                                  num_groups=5):
    world_size = 8
    actors, _ = create_collective_workers(world_size, backend=backend)
    for group_name in range(1, num_groups):
        ray.get([
            actor.init_group.remote(world_size, i, backend, str(group_name))
            for i, actor in enumerate(actors)
        ])
    for i in range(num_groups):
        group_name = "default" if i == 0 else str(i)
        results = ray.get([a.do_allreduce.remote(group_name) for a in actors])
        assert (results[0] == np.ones(
            (10, ), dtype=np.float32) * (world_size**(i + 1))).all()


@pytest.mark.parametrize("backend", [Backend.GLOO])
def test_allreduce_different_op(ray_start_distributed_2_nodes, backend):
    world_size = 8
    actors, _ = create_collective_workers(world_size, backend=backend)

    # check product
    ray.wait([
        a.set_buffer.remote(np.ones(10, dtype=np.float32) * (i + 2))
        for i, a in enumerate(actors)
    ])
    results = ray.get(
        [a.do_allreduce.remote(op=ReduceOp.PRODUCT) for a in actors])
    product = 1
    for i in range(world_size):
        product = product * (i + 2)
    assert (results[0] == np.ones((10, ), dtype=np.float32) * product).all()
    assert (results[1] == np.ones((10, ), dtype=np.float32) * product).all()

    # check min
    ray.wait([
        a.set_buffer.remote(np.ones(10, dtype=np.float32) * (i + 2))
        for i, a in enumerate(actors)
    ])
    results = ray.get([a.do_allreduce.remote(op=ReduceOp.MIN) for a in actors])
    assert (results[0] == np.ones((10, ), dtype=np.float32) * 2).all()
    assert (results[1] == np.ones((10, ), dtype=np.float32) * 2).all()

    # check max
    ray.wait([
        a.set_buffer.remote(np.ones(10, dtype=np.float32) * (i + 2))
        for i, a in enumerate(actors)
    ])
    results = ray.get([a.do_allreduce.remote(op=ReduceOp.MAX) for a in actors])
    assert (results[0] == np.ones((10, ), dtype=np.float32) * 9).all()
    assert (results[1] == np.ones((10, ), dtype=np.float32) * 9).all()


@pytest.mark.parametrize("backend", [Backend.GLOO])
@pytest.mark.parametrize("dtype",
                         [np.uint8, np.float16, np.float32, np.float64])
def test_allreduce_different_dtype(ray_start_distributed_2_nodes, dtype,
                                   backend):
    world_size = 8
    actors, _ = create_collective_workers(world_size, backend=backend)
    ray.wait([a.set_buffer.remote(np.ones(10, dtype=dtype)) for a in actors])
    results = ray.get([a.do_allreduce.remote() for a in actors])
    assert (results[0] == np.ones((10, ), dtype=dtype) * world_size).all()
    assert (results[1] == np.ones((10, ), dtype=dtype) * world_size).all()


@pytest.mark.parametrize("backend", [Backend.GLOO])
def test_allreduce_torch_numpy(ray_start_distributed_2_nodes, backend):
    # import torch
    world_size = 8
    actors, _ = create_collective_workers(world_size, backend=backend)
    ray.wait([actors[1].set_buffer.remote(torch.ones(10, ))])
    results = ray.get([a.do_allreduce.remote() for a in actors])
    assert (results[0] == np.ones((10, )) * world_size).all()

    ray.wait([actors[0].set_buffer.remote(torch.ones(10, ))])
    ray.wait([actors[1].set_buffer.remote(np.ones(10, dtype=np.float32))])
    results = ray.get([a.do_allreduce.remote() for a in actors])


if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v", "-x", __file__]))
