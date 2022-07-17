import cv2
import mediapipe as mp
import numpy as np
import pandas as pd


def predict_image_letters(images, model, cvt_color=True, static_image_mode=True, 
                          max_num_hands=2, min_detection_confidence=0.5):
    """
        images: array-like, a collection of cv2 images
            one image could have 0 or multiple landmarks
        model: classifier whose input is (62, ) features transfromed 
            from mediapipe hands' landmarks and predict class labels 0-25
        cvt_color: bool, if we need to convert cv2 colors

        return: list of tuples [(label_int, probability), ... ]
    """
    model_results = predict_image_hand_proba(
        images, model, cvt_color, static_image_mode, max_num_hands, min_detection_confidence
    )

    results = [
        (chr(ord('A') + label), p)
        for label, p in model_results
    ]

    return results


def predict_image_hand_proba(images, model, cvt_color=True, static_image_mode=True, 
                             max_num_hands=2, min_detection_confidence=0.5):
    """
        images: array-like, a collection of cv2 images
            one image could have 0 or multiple landmarks
        model: classifier whose input is (62, ) features transfromed 
            from mediapipe hands' landmarks
        cvt_color: bool, if we need to convert cv2 colors

        return: list of tuples [(label_int, probability), ... ]
    """
    features = images_to_landmark_features(
        images, cvt_color, static_image_mode, max_num_hands, min_detection_confidence
    )

    results = []
    for _ in features:
        if len(_) == 0:
            results.append((None, 0.0))
            continue
        
        prob = model.predict_proba(_)

        hand_idx = 0 if len(_) == 1 else np.argmax(np.max(prob, axis=1))
        prob = prob[hand_idx]
        results.append((np.argmax(prob), np.max(prob)))

    return results


def images_to_landmark_features(images, cvt_color=True, static_image_mode=True, 
                                max_num_hands=2, min_detection_confidence=0.5):
    """
        images: array-like, a collection of cv2 images
            one image could have 0 or multiple landmarks
        cvt_color: bool, if we need to convert cv2 colors

        return: list of features (X for the model)
            features: 2D array per image as an image can have multiple hand landmarks 
    """
    mp_hands = mp.solutions.hands

    features = []
    print(cvt_color, static_image_mode, max_num_hands, min_detection_confidence)
    with mp_hands.Hands(
        static_image_mode=static_image_mode,
        max_num_hands=max_num_hands,
        min_detection_confidence=min_detection_confidence
    ) as hands:
        for img in images:
            if cvt_color:            
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            mp_res = hands.process(img)
            landmarks = mp_res.multi_hand_world_landmarks

            features.append(np.array([
                landmark_to_features(_)
                for _ in landmarks
            ]))
       
    return features


def landmark_to_features(landmark):
    """
    Get normalize hand data per frame
    
    normalize landmarks coordinate + boundingbox feature engineering
    normalized X (20): MediaPipe features
    normalized Y (20): MediaPipe features
    normalized Z (20): MediaPipe features
    normalized Y/X, Z/X (2): engineered features
    
    :params landmark: mediapipe landmark for a single hand
    :return: np.array (62,)
    """
    origin_landmark_index = 0
    lm_orig = landmark.landmark[origin_landmark_index]
    lm_orig = [lm_orig.x, lm_orig.y, lm_orig.z]
    lm_coord = np.array([
        [_.x, _.y, _.z]
        for _ in landmark.landmark
    ])
    rng_xyz = (lm_coord.max(axis=0) - lm_coord.min(axis=0))

    return np.append(
        ((lm_coord - lm_orig) / rng_xyz.max())[1:].ravel(), 
        np.log(rng_xyz[1:] / rng_xyz[0])
    )




