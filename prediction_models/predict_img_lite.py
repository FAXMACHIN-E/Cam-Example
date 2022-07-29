import numpy as np


def predict_landmark_letters(landmarks, model):
    """
        landmarks: array-like, a collection mediapipe landmark for a single hand
        model: classifier whose input is (62, ) features transfromed 
            from mediapipe hands' landmarks

        return: list of tuples (letter, probability)
    """
    label, p = predict_landmark_hand_proba(landmarks, model)

    results = (
        chr(ord('A') + label)  if label is not None else None, 
        p
    ) 

    return results


def predict_landmark_hand_proba(landmarks, model):
    """
        landmarks: array-like, a collection mediapipe landmark for a single hand
        model: classifier whose input is (62, ) features transfromed 
            from mediapipe hands' landmarks

        return: tuples (label_int, probability)
    """
    if len(landmarks) == 0:
        return (None, 0.0)
    features = np.array([landmark_to_features(_) for _ in landmarks])

    prob = model.predict_proba(features)

    hand_idx = 0 if len(features) == 1 else np.argmax(np.max(prob, axis=1))
    prob = prob[hand_idx]
    return (np.argmax(prob), np.max(prob))


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
    lm_orig = landmark[origin_landmark_index]
    lm_orig = [lm_orig['x'], lm_orig['y'], lm_orig['z']]
    lm_coord = np.array([
        [_['x'], _['y'], _['z']] for _ in landmark
    ])
    rng_xyz = (lm_coord.max(axis=0) - lm_coord.min(axis=0))

    return np.append(
        ((lm_coord - lm_orig) / rng_xyz.max())[1:].ravel(), 
        np.log(rng_xyz[1:] / rng_xyz[0])
    )




