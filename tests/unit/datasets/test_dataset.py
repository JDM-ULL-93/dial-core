# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import numpy as np
import pytest

from dial_core.datasets import Dataset

np.random.seed(0)


def test_empty_dataset(empty_dataset):
    x, y = empty_dataset.head(10)

    assert len(x) == 0
    assert len(y) == 0


def test_input_shape(simple_array_dataset):
    assert simple_array_dataset.input_shape == (3,)


def test_output_shape(simple_array_dataset):
    assert simple_array_dataset.output_shape == ()


def test_head(simple_numeric_dataset):
    x, y = simple_numeric_dataset.head(2)

    assert x.tolist() == [1, 2]
    assert y.tolist() == [10, 20]


def test_head_with_more_elements(simple_numeric_dataset):
    x, y = simple_numeric_dataset.head(10000)

    assert x.tolist() == [1, 2, 3, 4]
    assert y.tolist() == [10, 20, 30, 40]


def test_items(simple_numeric_dataset):
    x, y = simple_numeric_dataset.items(1, 3)

    assert x.tolist() == [2, 3]
    assert y.tolist() == [20, 30]


def test_items_with_more_elements(simple_numeric_dataset):
    x, y = simple_numeric_dataset.items(1, 2000)

    assert x.tolist() == [2, 3, 4]
    assert y.tolist() == [20, 30, 40]


def test_item_backwards_start(simple_numeric_dataset):
    x, y = simple_numeric_dataset.items(start=-2)
    assert x.tolist() == [3, 4]
    assert y.tolist() == [30, 40]


def test_item_backwards_end(simple_numeric_dataset):
    x, y = simple_numeric_dataset.items(end=-2)

    assert x.tolist() == [1, 2]
    assert y.tolist() == [10, 20]


def test_get_batch(simple_numeric_dataset):
    simple_numeric_dataset.batch_size = 2

    bx, by = simple_numeric_dataset[0]

    assert bx.tolist() == [1, 2]
    assert by.tolist() == [10, 20]

    bx, by = simple_numeric_dataset[1]

    assert bx.tolist() == [3, 4]
    assert by.tolist() == [30, 40]


def test_delete_rows(simple_numeric_dataset):
    assert simple_numeric_dataset.row_count() == 4

    simple_numeric_dataset.delete_rows(0)

    x, y = simple_numeric_dataset.head(3)

    assert x.tolist() == [2, 3, 4]
    assert y.tolist() == [20, 30, 40]
    assert simple_numeric_dataset.row_count() == 3

    """
        Modificacion.
            Autor: JDM 10/03/2021
            Description:
                De --> "simple_numeric_dataset.delete_rows(1, 20)"
                A -->  "simple_numeric_dataset.delete_rows(1, 2)"
            Reason: 
                Existia un 'typo' por el cual se asignaba a borrar 20 elementos,
                cuando el array solo tenia 3.
    """
    simple_numeric_dataset.delete_rows(1, 2)

    x, y = simple_numeric_dataset.head(3)

    assert x.tolist() == [2]
    assert y.tolist() == [20]
    assert simple_numeric_dataset.row_count() == 1


def test_delete_rows_array(simple_array_dataset):
    assert simple_array_dataset.row_count() == 3

    simple_array_dataset.delete_rows(1)

    x, y = simple_array_dataset.head(3)

    assert x.tolist() == [[1, 1, 1], [3, 3, 3]]
    assert y.tolist() == [1, 3]


def test_insert_rows(simple_numeric_dataset):
    assert simple_numeric_dataset.row_count() == 4

    simple_numeric_dataset.insert(1, x=[9], y=[90])

    x, y = simple_numeric_dataset.head(3)

    assert x.tolist() == [1, 9, 2]
    assert y.tolist() == [10, 90, 20]


def test_insert_rows_different_length(simple_numeric_dataset):
    assert simple_numeric_dataset.row_count() == 4

    with pytest.raises(ValueError):
        simple_numeric_dataset.insert(1, x=[9, 5, 6], y=[90])


def test_insert_rows_arrays(simple_array_dataset):
    assert simple_array_dataset.row_count() == 3

    simple_array_dataset.insert(
        0, x=[np.array([5, 5, 5]), np.array([6, 6, 6])], y=[5, 6],
    )

    x, y = simple_array_dataset.head(3)

    assert x.tolist() == [[5, 5, 5], [6, 6, 6], [1, 1, 1]]
    assert y.tolist() == [5, 6, 1]


def test_get_irregular_batches(simple_numeric_dataset):
    simple_numeric_dataset.batch_size = 3

    bx, by = simple_numeric_dataset[0]

    assert bx.tolist() == [1, 2, 3]
    assert by.tolist() == [10, 20, 30]

    bx, by = simple_numeric_dataset[1]

    assert bx.tolist() == [4]
    assert by.tolist() == [40]


def test_process_roles(simple_categorical_dataset):
    x, y = simple_categorical_dataset.head(3, Dataset.Role.Raw)

    assert x.tolist() == [0, 1, 2]
    assert y.tolist() == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    x, y = simple_categorical_dataset.head(3, Dataset.Role.Display)

    assert x.tolist() == ["0", "1", "2"]
    assert y.tolist() == ["foo", "bar", "hue"]


def test_transformer_functions(simple_numeric_dataset):
    x_transformations = [lambda x: x * 2, lambda x: x + 2]
    y_transformations = [lambda y: y / 10, lambda y: y + 10]

    simple_numeric_dataset.x_type.transformations = x_transformations
    simple_numeric_dataset.y_type.transformations = y_transformations

    x, y = simple_numeric_dataset.head(3)

    assert x.tolist() == [4, 6, 8]
    assert y.tolist() == [11, 12, 13]


def test_pickable(simple_numeric_dataset):
    obj = pickle.dumps(simple_numeric_dataset)
    pickle.loads(obj)
