from base64 import b64encode
from sklearn.decomposition import PCA

import io
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import time


class PCAHandler:

    def __init__(self, labels, data):
        self.labels = labels
        self.data = data

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

        fig = plt.figure(1, figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d", elev=-150, azim=110)
        scatter = ax.scatter(
            reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2], c=colors, s=40
        )
        ax.set_title("3D PCA Reduction")
        ax.set_xlabel("1st component")
        # ax.xaxis.set_ticklabels([])
        ax.set_ylabel("2nd component")
        # ax.yaxis.set_ticklabels([])
        ax.set_zlabel("3rd component")

        _ = ax.legend(
            scatter.legend_elements()[0], self.labels.unique(), loc="upper right"
        )

        buf = io.BytesIO()

        plt.savefig(buf, format="png", bbox_inches="tight")
        b64_image = b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
        # plt.savefig("PCA.png", format="png", bbox_inches="tight")

        self.model = pca

        return {
            "Method": "PCA 3D",
            "Explained Variance": pca_variance.explained_variance_.tolist(),
            "Principal Components": report_df.to_dict(),
            "image": b64_image,
            "Solution Time": solve_time,
        }

    def sample_prediction(self, new_data):
        return self.pca.transform(new_data)

    def save_model(self):
        raise NotImplementedError
