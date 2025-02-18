from base64 import b64encode
from sklearn.decomposition import PCA

import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


class PCAHandler:

    def __init__(self, labels, data):
        self.labels = labels
        self.data = data

    def create_image(self, new_point=None):

        fig = plt.figure(1, figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d", elev=-150, azim=110)
        data = self.modeled_data["data"]
        colors = self.modeled_data["colors"]

        if new_point is not None:
            data = np.concatenate((data, new_point), axis=0)
            colors = np.append(colors, 2)
            labels = self.labels.unique()
            labels = np.append(labels, "New sample")
        else:
            labels = self.labels.unique()

        scatter = ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colors, s=40)

        ax.set_title("3D PCA Reduction")
        ax.set_xlabel("1st component")
        # ax.xaxis.set_ticklabels([])
        ax.set_ylabel("2nd component")
        # ax.yaxis.set_ticklabels([])
        ax.set_zlabel("3rd component")

        _ = ax.legend(
            scatter.legend_elements()[0], labels, loc="upper right"
        )

        buf = io.BytesIO()

        plt.savefig(buf, format="png", bbox_inches="tight")
        b64_image = b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
        # plt.savefig("PCA.png", format="png", bbox_inches="tight")

        return b64_image

    def train_model(self):
        pca = PCA(n_components=3)
        start = time.time()
        pca_variance = pca.fit(self.data)
        reduced_data = pca.fit_transform(self.data)
        solve_time = time.time() - start

        ### Not needed?
        # self.pca = pca

        # print(
        #     f"PCA: Explained variance ratios -\n{pca_variance.explained_variance_ratio_}"
        # )
        colors = self.labels.apply(lambda x: 0 if x == "R" else 1)

        report_df = pd.DataFrame(
            reduced_data, columns=["Factor 1", "Factor 2", "Factor 3"]
        )

        report_df["Labels"] = self.labels
        report_df["Colors"] = colors

        # print("-" * 80)
        # print(f"Joined data:\n{report_df}")
        # print("-" * 80)

        self.model = pca
        self.modeled_data = {"data": reduced_data, "colors": colors}

        b64_image = self.create_image()

        return {
            "Method": "PCA 3D",
            "Explained Variance": pca_variance.explained_variance_.tolist(),
            "Principal Components": report_df.to_dict(),
            "image": b64_image,
            "Solution Time": solve_time,
        }

    def sample_prediction(self, new_data):
        new_point = self.model.transform(new_data)
        b64_image = self.create_image(new_point=new_point)
        return {
            "image": b64_image,
            "point": new_point.tolist(),
        }

    def save_model(self):
        raise NotImplementedError
