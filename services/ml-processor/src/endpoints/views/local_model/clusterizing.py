from sentence_transformers import util


def custom_distance(x, y):
    return 1 - util.cos_sim(x, y)[0][0].item()


