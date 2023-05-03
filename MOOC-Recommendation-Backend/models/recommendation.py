import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error

from matplotlib.backends.backend_pdf import PdfPages

tags_file = '/Users/paulthompson/Documents/MSAN_Files/Spr2_Distributed/HW1/movies/tags.txt'
ratings_file = '/Users/paulthompson/Documents/MSAN_Files/Spr2_Distributed/HW1/movies/ratings.txt'
movies_file = '/Users/paulthompson/Documents/MSAN_Files/Spr2_Distributed/HW1/movies/movies.txt'


# def getInitialMatrix(A):
#     '''
#     Gets data from files and creates user-item matrices
#     :return: A, R user-item matrices
#     '''
#     print(" 'A' matrix shape is", A.shape)
#
#     print("Getting 'R' Binary Matrix of rating or no rating...")
#     R = A > 0
#
#     R.replace(True, 1.0, inplace=True)
#     R.replace(False, 0.0, inplace=True)
#     # R[R == True] = 1
#     # R[R == False] = 0
#     R = R.astype(np.float64, copy=False)
#
#     return A, R
#
#
# def runALS(A, R, n_factors, n_iterations, lambda_):
#     '''
#     Runs Alternating Least Squares algorithm in order to calculate matrix.
#     :param A: User-Item Matrix with ratings
#     :param R: User-Item Matrix with 1 if there is a rating or 0 if not
#     :param n_factors: How many factors each of user and item matrix will consider
#     :param n_iterations: How many times to run algorithm
#     :param lambda_: Regularization parameter
#     :return:
#     '''
#     print("Initiating ")
#     lambda_ = 0.1
#     n_factors = 3
#     n, m = A.shape
#     n_iterations = 20
#     Users = 3 * np.random.rand(n, n_factors)
#     Items = 3 * np.random.rand(m, n_factors)
#
#     def get_error(A, Users, Items, R):
#         # This calculates the MSE of nonzero elements
#         return np.sum((R * (A - np.dot(Users, Items))) ** 2) / np.sum(R)
#
#     MSE_List = []
#
#     print("Starting Iterations")
#     for iter in range(n_iterations):
#         for i, Ri in R.iterrows():
#             Users[i] = np.linalg.solve(np.dot(Items, np.dot(np.diag(np.array(Ri)), Items.T)) + lambda_ * np.eye(n_factors),
#                                        np.dot(Items, np.dot(np.diag(np.array(Ri)), A[i].T))).T
#         print("Error after solving for User Matrix:", get_error(A, Users, Items, R))
#
#         for j, Rj in enumerate(R.T):
#             Items[:, j] = np.linalg.solve(np.dot(Users.T, np.dot(np.diag(Rj), Users)) + lambda_ * np.eye(n_factors),
#                                           np.dot(Users.T, np.dot(np.diag(Rj), A[:, j])))
#         print("Error after solving for Item Matrix:", get_error(A, Users, Items, R))
#
#         MSE_List.append(get_error(A, Users, Items, R))
#         print('%sth iteration is complete...' % iter)
#
#     print(MSE_List)
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     plt.plot(range(1, len(MSE_List) + 1), MSE_List)
#     plt.ylabel('Error')
#     plt.xlabel('Iteration')
#     plt.title('Python Implementation MSE by Iteration \n with %d users and %d movies' % A.shape)
#     plt.savefig('Python MSE Graph.pdf', format='pdf')
#     plt.show()


# if __name__ == '__main__':
#     A, R = getInitialMatrix()
#     runALS(A, R, n_factors=3, n_iterations=20, lambda_=.1)

class ExplicitMF:
    """
    Train a matrix factorization models using Alternating Least Squares
    to predict empty entries in a matrix

    Parameters
    ----------
    n_iters : int
        number of iterations to train the algorithm

    n_factors : int
        number of latent factors to use in matrix
        factorization models, some machine-learning libraries
        denote this as rank

    reg : float
        regularization term for item/user latent factors,
        since lambda is a keyword in python we use reg instead
    """

    def __init__(self, n_iters, n_factors, reg):
        self.reg = reg
        self.n_iters = n_iters
        self.n_factors = n_factors

    def fit(self, train, test):
        """
        pass in training and testing at the same time to record
        models convergence, assuming both dataset is in the form
        of User x Item matrix with cells as ratings
        """
        self.n_user, self.n_item = train.shape
        self.user_factors = np.random.random((self.n_user, self.n_factors))
        self.item_factors = np.random.random((self.n_item, self.n_factors))

        # record the training and testing mse for every iteration
        # to show convergence later (usually, not worth it for production)
        self.test_mse_record = []
        self.train_mse_record = []
        for _ in range(self.n_iters):
            self.user_factors = self._als_step(train, self.user_factors, self.item_factors)
            self.item_factors = self._als_step(train.T, self.item_factors, self.user_factors)
            predictions = self.predict()
            test_mse = self.compute_mse(test, predictions)
            train_mse = self.compute_mse(train, predictions)
            self.test_mse_record.append(test_mse)
            self.train_mse_record.append(train_mse)

        return self

    def _als_step(self, ratings, solve_vecs, fixed_vecs):
        """
        when updating the user matrix,
        the item matrix is the fixed vector and vice versa
        """
        A = fixed_vecs.T.dot(fixed_vecs) + np.eye(self.n_factors) * self.reg
        b = ratings.dot(fixed_vecs)
        A_inv = np.linalg.inv(A)
        solve_vecs = b.dot(A_inv)
        return solve_vecs

    def predict(self):
        """predict ratings for every user and item"""
        pred = self.user_factors.dot(self.item_factors.T)
        return pred

    @staticmethod
    def compute_mse(y_true, y_pred):
        """ignore zero terms prior to comparing the mse"""
        mask = np.nonzero(y_true)
        mse = mean_squared_error(y_true[mask], y_pred[mask])
        return mse


def plot_learning_curve(model):
    """visualize the training/testing loss"""
    linewidth = 3
    plt.plot(model.test_mse_record, label='Test', linewidth=linewidth)
    plt.plot(model.train_mse_record, label='Train', linewidth=linewidth)
    plt.xlabel('iterations')
    plt.ylabel('MSE')
    plt.legend(loc='best')

    plt.savefig("models.png")


def create_train_test(ratings):
    """
    split into training and test sets,
    remove 10 ratings from each user
    and assign them to the test set
    """
    test = np.zeros(ratings.shape)
    train = ratings.copy()
    for user in range(ratings.shape[0]):
        flatnonezero = np.flatnonzero(ratings[user])
        if flatnonezero.size:
            test_index = np.random.choice(flatnonezero, size=2, replace=False)

            train[user, test_index] = 0.0
            test[user, test_index] = ratings[user, test_index]

    # assert that training and testing set are truly disjoint
    assert np.all(train * test == 0)
    return train, test
