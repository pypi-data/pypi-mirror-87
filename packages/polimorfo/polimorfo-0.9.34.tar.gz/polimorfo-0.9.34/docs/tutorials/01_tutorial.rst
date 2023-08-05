.. code:: ipython3

    import sys
    sys.path.append('..')

.. code:: ipython3

    %load_ext autoreload
    %autoreload 2

.. code:: ipython3

    from polimorfo.datasets import CocoDataset, ExportFormat, SemanticCocoDataset
    import matplotlib.pyplot as plt
    from polimorfo.utils import maskutils
    import numpy as np
    from skimage import measure

.. code:: ipython3

    ds = SemanticCocoDataset('../../car-models/datasets/carparts_cropped_all/val_carparts_dataset.json')


.. parsed-literal::

    load categories: 100%|██████████| 42/42 [00:00<00:00, 177046.00it/s]
    load images: 100%|██████████| 500/500 [00:00<00:00, 958917.24it/s]
    load annotations: 100%|██████████| 5824/5824 [00:00<00:00, 1297685.22it/s]


.. code:: ipython3

    ds.show_image()




.. parsed-literal::

    <AxesSubplot:>




.. image:: 01_tutorial_files/01_tutorial_4_1.png


.. code:: ipython3

    fig = ds.show_images([481, 125, 101, 74])



.. image:: 01_tutorial_files/01_tutorial_5_0.png


.. code:: ipython3

    masks = ds.get_segmentation_mask(10)

.. code:: ipython3

    masks

.. code:: ipython3

    plt.matshow(np.array(masks))

.. code:: ipython3

    np.unique(np.array(masks))

.. code:: ipython3

    test_mask = ((np.array(masks) == 4).astype(int) * 4) + ((np.array(masks) == 37).astype(int) * 4)

.. code:: ipython3

    test_mask

.. code:: ipython3

    plt.matshow(test_mask)

.. code:: ipython3

    test_mask.shape

.. code:: ipython3

    img_id = ds.add_image('../../car-models/datasets/carparts_cropped_all/images/' + ds.imgs[10]['file_name'])

.. code:: ipython3

    img_id

.. code:: ipython3

    test_mask.shape

.. code:: ipython3

    probs = np.random.rand(2, *test_mask.shape)

.. code:: ipython3

    ann_idxs = ds.add_semantic_annotation(img_id, test_mask, probs)
    ann_idxs

.. code:: ipython3

    ds.anns[5825].keys()

.. code:: ipython3

    p = ds.anns[5825]['segmentation']

.. code:: ipython3

    m = maskutils.polygons_to_mask(p, *test_mask.shape)

.. code:: ipython3

    plt.matshow(m)

.. code:: ipython3

    ds.show_image(img_id)


.. code:: ipython3

    probs


.. code:: ipython3

    import json
    import numpy as np
    from pycocotools import mask
    from skimage import measure
    
    ground_truth_binary_mask = np.array([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                         [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                         [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
                                         [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
                                         [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
                                         [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
                                         [  1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                         [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                         [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=np.uint8)
    
    fortran_ground_truth_binary_mask = np.asfortranarray(ground_truth_binary_mask)
    encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask)
    ground_truth_area = mask.area(encoded_ground_truth)
    ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
    contours = measure.find_contours(ground_truth_binary_mask, 0.5)
    
    annotation = {
            "segmentation": [],
            "area": ground_truth_area.tolist(),
            "iscrowd": 0,
            "image_id": 123,
            "bbox": ground_truth_bounding_box.tolist(),
            "category_id": 1,
            "id": 1
        }
    
    for contour in contours:
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        annotation["segmentation"].append(segmentation)
        
    print(json.dumps(annotation, indent=4))

