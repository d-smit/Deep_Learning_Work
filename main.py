__author__ = 'Team Alpha'

from imdb import IMDb
from fashion import Fashion

def main(dataset):
    if dataset == 0:
        Fashion(
            combination=1,
            learning_rate=0.001,
            epochs=1,
            batches=250,
            seed=12345
        )
        
    elif dataset == 1:
        IMDb(
<<<<<<< HEAD
            combination=1,
            learning_rate=0.04,
            epochs=2,
=======
            combination=2,
            learning_rate=0.05,
            epochs=1,
>>>>>>> a10f1d5784e886ceedd67f6b563c223d1d449207
            batches=400,
            seed=12345
        )


if __name__ == "__main__":
    main(0)
