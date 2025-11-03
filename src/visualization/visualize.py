import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display

# --------------------------------------------------------------
# Load data

df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot single columns

set_df = df[df["set"] == 1]

for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop=True), label="acc_y")
    plt.legend()
    break

for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label="acc_y")
    plt.legend()
    break

# --------------------------------------------------------------
# Adjust plot settings

mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets

category_df = df.query("label == 'squat'").query("participant == 'A'").reset_index()

fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Compare participants

participant_df = df.query("label == 'bench'").sort_values("participant").reset_index()

fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis

label = "squat"
participant = "A"
all_axis_df = (
    df.query(f"label == '{label}'")
    .query(f"participant == '{participant}'")
    .reset_index()
)

fig, ax = plt.subplots()
all_axis_df[["acc_y", "acc_x", "acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor

labels = df["label"].unique()
participants = df["participant"].unique()

for label in labels:
    for participant in participants:
        all_axis_df = (
            df.query(f"label == '{label}'")
            .query(f"participant == '{participant}'")
            .reset_index()
        )

        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["acc_y", "acc_x", "acc_z"]].plot(ax=ax)
            ax.set_ylabel("acc_y")
            ax.set_xlabel("samples")
            plt.title(f"{label} ({participant})".title())
            plt.legend()
        break
    break

for label in labels:
    for participant in participants:
        all_axis_df = (
            df.query(f"label == '{label}'")
            .query(f"participant == '{participant}'")
            .reset_index()
        )

        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["gyr_y", "gyr_x", "gyr_z"]].plot(ax=ax)
            ax.set_ylabel("gyr_y")
            ax.set_xlabel("samples")
            plt.title(f"{label} ({participant})".title())
            plt.legend()
        break
    break

# --------------------------------------------------------------
# Combine plots in one figure

label = "row"
participant = "A"
combined_plot_df = (
    df.query(f"label == '{label}'")
    .query(f"participant == '{participant}'")
    .reset_index(drop=True)
)

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
combined_plot_df[["acc_y", "acc_x", "acc_z"]].plot(ax=ax[0])
combined_plot_df[["gyr_y", "gyr_x", "gyr_z"]].plot(ax=ax[1])

ax[0].legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True
)
ax[1].legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True
)
ax[1].set_xlabel("samples")

# --------------------------------------------------------------
# Main output
# Loop over all combinations and export for both sensors

labels = df["label"].unique()
participants = df["participant"].unique()

# Ensure save directory exists
output_dir = "../../reports/figures"
os.makedirs(output_dir, exist_ok=True)

for label in labels:
    for participant in participants:
        combined_plot_df = (
            df.query(f"label == '{label}'")
            .query(f"participant == '{participant}'")
            .reset_index(drop=True)
        )

        # Skip empty combinations
        if combined_plot_df.empty:
            continue

        # Create figure
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))

        # Plot accelerometer and gyroscope data
        combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
        combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

        ax[0].set_title(f"{label.title()} ({participant}) - Accelerometer")
        ax[1].set_title(f"{label.title()} ({participant}) - Gyroscope")

        ax[0].legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            ncol=3,
            fancybox=True,
            shadow=True,
        )
        ax[1].legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            ncol=3,
            fancybox=True,
            shadow=True,
        )

        ax[1].set_xlabel("Samples")

        # Sanitize filename
        safe_label = str(label).replace("/", "-").replace("..", "")
        safe_participant = str(participant).split("/")[-1]
        filename = f"{safe_label.title()} ({safe_participant}).png"

        # Save to reports/figures/
        save_path = os.path.join(output_dir, filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close(fig)  # prevents memory buildup

        print(f"✅ Saved: {save_path}")
