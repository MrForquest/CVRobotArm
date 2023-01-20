import cv2
import mediapipe as freedomtech

drawingModule = freedomtech.solutions.drawing_utils
handsModule = freedomtech.solutions.hands

mod = handsModule.Hands()


def findpostion(frame1):
    """
    get the position of the fingers
    """
    postion_book = dict()
    results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
            postion_book = dict()
            for id, pt in enumerate(handLandmarks.landmark):
                postion_book[id] = pt

    return postion_book


def dist_bpt(pt1, pt2):
    """
    get distance between two points in space

    Parameters
        ----------
        pt1 : mediapipe.framework.formats.landmark_pb2.NormalizedLandmark
            first point
        pt2 : mediapipe.framework.formats.landmark_pb2.NormalizedLandmark
            second point

        Returns
        -------
        int
           distance two points
    """

    axes = ["x", "y", "z"]
    return sum([(getattr(pt1, ax) - getattr(pt2, ax)) ** 2 for ax in axes]) ** 0.5


class Hand:
    fingers_ids = [4, 8, 12, 16, 20]  # id пальцев
    start_ids = [17, 0, 0, 0, 0]  # участки руки, от которых считаются расстояния для каждого модуля
    max_dists = {4: 1.1522183355496327, 8: 1.8763855577473698, 12: 1.980128835021695,
                 16: 1.9121189123789621, 20: 1.577292708116198}  # максимальные значния расстояния
    min_dists = {4: 0.52123644525618, 8: 1.0275975294985669, 12: 0.9472953967035629,
                 16: 0.8117076673451709, 20: 0.8049819295697188}  # минимальные значния расстояния
    dist_borders = dict()  # расстояния-границы
    # если расстояние пальца меньше расстояния-границы для этого пальца, то палец загнут

    for fing_id in fingers_ids:
        dist_borders[fing_id] = (max_dists[fing_id] + min_dists[fing_id]) / 2

    def get_fingers_state(self, frame):
        """
        Parameters
        ----------
        frame : numpy.ndarray
            frame

        Returns
        -------
        dict
            dictionary with the condition of the fingers.
        """
        all_positions = findpostion(frame)
        if all_positions:
            dists_fings = dict()
            wrist = all_positions[0]
            dists = list()
            states_fingers = dict()

            pt_wrist = all_positions[0]
            pt_mcp = all_positions[5]
            base_dist = dist_bpt(pt_mcp, pt_wrist)
            for i, fing_id in enumerate(self.fingers_ids):
                dists_fings[fing_id] = dist_bpt(all_positions[fing_id],
                                                all_positions[self.start_ids[i]]) / base_dist
                states_fingers[fing_id] = int(dists_fings[fing_id] < self.dist_borders[fing_id])
            return states_fingers
        else:
            return None
