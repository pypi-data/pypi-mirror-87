# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxvis',
 'pyxvis.features',
 'pyxvis.geometry',
 'pyxvis.io',
 'pyxvis.learning',
 'pyxvis.processing',
 'pyxvis.processing.helpers',
 'pyxvis.simulation']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0',
 'numpy<1.19',
 'opencv-contrib-python>=3.4.0,<3.5.0',
 'opencv-python>=3.4.0,<3.5.0',
 'pandas>=1.1.2,<2.0.0',
 'pybalu>=0.2.9,<0.3.0',
 'pyqt5>=5.15.1,<6.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.5.2,<2.0.0',
 'tensorflow>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'pyxvis',
    'version': '0.1.0a5',
    'description': 'Python package for Xvis toolbox',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/hypermodern-python.svg)](https://pypi.org/project/hypermodern-python/)\n\n# py-XVis\n\nPython implementation for XVis Toolbox release with the book Computer Vision for X-Ray Testing. Originally implemented \nin Matlab by Domingo Mery for the first edition of the book. This package is part of the second edition of the book \nComputer Vision for X-Ray Testing (November 2020).\n\n\n# Requirements\n\n- Python 3.6 or higher\n- numpy < 1.19\n- matplotlib >= 3.3.2\n- scipy >= 1.5.2\n- pyqt5 >= 5.15.1\n- pybalu >= 0.2.9\n- opencv-python = 3.4.2\n- opencv-contrib-python = 3.4.2\n- tensorflow >= 2.3.1 \n- scikit-learn >= 0.23.2\n- scikit-image >= 0.17.2\n- pandas >= 1.1.2\n\n\n# Instalation\nThe package is part of the Python Index (PyPi). Installation is available by pip:\n\n`pip install pyxvis`\n\n\n\n# Interactive Examples\n\nAll examples in the Book have been implemented in Jupyter Notebooks tha run on Google Colab.\n\n\n## Chapter 01: X-ray Testing [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1meevAFZkZ_0SUBPYqo_nl7grBcqfeVMP?usp=sharing)\n\n* Example 1.1: Displaying X-ray images\n* Example 1.2: Dual Energy\n* Example 1.3: Help of PyXvis functions\n\n\n## Chapter 02: Images for X-ray Testing [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1MDc5wbH11I5PV18l5ZSt92yugz0eHi4W?usp=sharing)\n\n* Example 2.1: Displaying an X-ray image of GDXray\n\n\n## Chapter 03: Geometry in X-ray Testing [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14CgSCGcpm4Wc4SbVB70iBx6Cw6rXoZAq?usp=sharing)\n\n* Example 3.1: Euclidean 2D transformation\n* Example 3.2: Euclidean 3D transformation\n* Example 3.3: Perspective projection\n* Example 3.4: Cubic model for distortion correction\n* Example 3.5: Hyperbolic model for imaging projection\n* Example 3.6: Geometric calibration\n* Example 3.7: Epipolar geometry\n* Example 3.8: Trifocal geometry\n* Example 3.9: 3D reconstruction\n\n\n## Chapter 04: X-ray Image Processing [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1edbph3qfb2PfKOWPGUWUsC0DeX8muO9U?usp=sharing)\n\n* Example 4.1: Aritmetic average of images\n* Example 4.2: Contrast enhancement\n* Example 4.3: Shading correction\n* Example 4.4: Detection of defects using median filtering\n* Example 4.5: Edge detection using gradient operation\n* Example 4.6: Edge detection with LoG\n* Example 4.7: Segmentation of bimodal images\n* Example 4.8: Welding inspection using adaptive thresholding\n* Example 4.9: Region growing\n* Example 4.10: Defects detection using LoG approach\n* Example 4.11: Segmentation using MSER\n* Example 4.12: Image restoration\n\n\n## Chapter 05: X-ray Image Representation [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dwGTGHA1CR1om3MirGX5VCVhQgVc-g3-?usp=sharing)\n\n* Example 5.1: Geometric features\n* Example 5.2: Elliptical features\n* Example 5.3: Invariant moments\n* Example 5.4: Intenisty features\n* Example 5.5: Defect detection usin contrast features\n* Example 5.6: Crossing line profiles (CLP)\n* Example 5.7: SIFT\n* Example 5.8: feature se;ection\n* Example 5.9: Example using intenisty features\n* Example 5.10: Example using geometric features\n\n\n## Chapter 06: Classification in X-ray Testing [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zGx0HpAt7EtOiORXkTluOPDW4w5alNSj?usp=sharing)\n\n* Example 6.1: Basic classification example\n* Example 6.2: Minimal distance (dmin)\n* Example 6.3: Bayes\n* Example 6.4: Mahalanobis, LDA and QDA\n* Example 6.5: KNN\n* Example 6.6: Neural networks\n* Example 6.7: Support Vector Machines (SVM)\n* Example 6.8: Training and testing many classifiers\n* Example 6.9: Hold-out\n* Example 6.10: Cross-validation\n* Example 6.11: Confusion matrix\n* Example 6.12: ROC and Precision-Recall curves\n* Example 6.13: Example with intensity features\n* Example 6.14: Example with geometric features\n\n\n## Chapter 07: Deep Learing in X-ray Testing\n\n* Example 7.1: Basic neural networks (from skratch) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Ohs0hBDu5zRtNagbqBCJV6fmxq63CxS6?usp=sharing)\n\n* Example 7.2: Neural network using sklearn [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Ohs0hBDu5zRtNagbqBCJV6fmxq63CxS6?usp=sharing)\n\n* Example 7.3: Convolutional Neural Network [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1nI3AABdBJKdT680L-ouUwX3ywpajv8bC?usp=sharing)\n\n* Example 7.4: Pre-trained models [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1JA3sgXqDHN7gkAdv1dRa-a-IgsArAA2M?usp=sharing)\n\n* Example 7.5: Fine tunning [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1iC_XLsyBru3I2RpJot8YCGt_AbQNw3mz?usp=sharing)\n\n* Example 7.6: Generative Adversarial Networks (GANs) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Bv9wptpLuxjXxcx6UQmPGtLdZvx949iU?usp=sharing)\n\n* Example 7.7: Object detection using YOLOv3 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TUBRa4kal-chsQHvstIL2ZeNZ24PJotC?usp=sharing)\n\n* Example 7.8: Object detection using YOLOv4 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1S07jBiG1No6cq2mx8XnEV0XuToljpxs_?usp=sharing)\n\n* Example 7.9: Object detection using YOLOv5 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1D6j2bk5uzUIJE0MQXjiyEDvh9wEEmDUJ?usp=sharing)\n\n* Example 7.10: Object detection using EfficientDet [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1EmTQ02IwXmJQ7082ooh834IYyQyxZcAL?usp=sharing)\n\n* Example 7.11: Object detection using RetinaNet [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1H7HnECaEuPIwIGWQb2vRu-eUx1LGkaa_?usp=sharing)\n\n* Example 7.12: Object detection using DETR [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1vuzCI6zE8KD3xuaS1lsCFkZKdd6NBDcY?usp=sharing)\n\n* Example 7.13: Object detection using SSD [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1PFlw9MA5z7vsUvYCA1H83bLtZRW5Zxp2?usp=sharing)\n\n\n## Chapter 08: Simulation in X-ray Testing [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1s7bKncSrQhIq_kW0qO3JvUOyyK8rfp3Q?usp=sharing)\n\n* Example 8.1: Basic simulation using voxels\n* Example 8.2: Simulation of defects using mask\n* Example 8.3: Simulation of ellipsoidal defects\n* Example 8.4: Superimposition of threat objects\n\n\n## Chapter 09: Applications in X-ray Testing\n\n* Example 9.1: Defect detection in castings [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1FLyUEYrevSu3RbZQaoPsd2BMG4MvRew0?usp=sharing)\n\n* Example 9.2: Defect detection in welds [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mFiaoEsuhAEQoev_jgPEv35G1lIt55F8?usp=sharing)\n\n',
    'author': 'Christian Pieringer',
    'author_email': '8143906+cpieringer@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
