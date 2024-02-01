import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

df = pd.read_csv('plan_csv/16701570.csv')

# Define a color for each unique in_product_family value
unique_families = df['in_product_family'].unique()
colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_families)))
color_dict = dict(zip(unique_families, colors))

# Create a Patch object for each unique in_product_family value
patches = [mpatches.Patch(color=color_dict[family], label=family) for family in unique_families]

# Plot the room layout from the outer bounding box coordinates of the room.
room = df[df['in_product_family'] == 'ROOM'].iloc[0]
outer_bounding_box = room[
    ['out_bounding_box_x1', 'out_bounding_box_y1', 'out_bounding_box_x2', 'out_bounding_box_y2', 'out_bounding_box_x3',
     'out_bounding_box_y3', 'out_bounding_box_x4', 'out_bounding_box_y4']].values
outer_bounding_box = outer_bounding_box.reshape(-1, 2)
outer_bounding_box = np.vstack([outer_bounding_box, outer_bounding_box[0]])  # Close the shape

# Plotting the outer bounding box of the room
plt.figure(figsize=(14, 12))
plt.plot(outer_bounding_box[:, 0], outer_bounding_box[:, 1], '-o')

# Plot the objects within the room using the outer bounding box coordinates.
for _, row in df.iterrows():
    if row['in_product_family'] != 'ROOM':  # We don't need to plot the room again
        object_bounding_box = row[
            ['out_bounding_box_x1', 'out_bounding_box_y1', 'out_bounding_box_x2', 'out_bounding_box_y2',
             'out_bounding_box_x3', 'out_bounding_box_y3', 'out_bounding_box_x4', 'out_bounding_box_y4']].values
        object_bounding_box = object_bounding_box.reshape(-1, 2)
        object_bounding_box = np.vstack([object_bounding_box, object_bounding_box[0]])  # Close the shape
        plt.plot(object_bounding_box[:, 0], object_bounding_box[:, 1], '-o',
                 color=color_dict[row['in_product_family']])  # Plot with lines and markers
        plt.fill(object_bounding_box[:, 0], object_bounding_box[:, 1], color=color_dict[row['in_product_family']],
                 alpha=0.4)  # Fill for better visualization
        plt.text(object_bounding_box[0, 0], object_bounding_box[0, 1], row['in_product_family'], fontsize=8,
                 verticalalignment='top', color='black')

# Add the legend to the plot
plt.legend(handles=patches, bbox_to_anchor=(1.0, 1), loc='upper left',
           title='Product Families')  # Adjust the position of the legend

# Final plot adjustments
plt.gca().invert_yaxis()
plt.title('Room Layout with Objects')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.savefig('room_layout.png', dpi=300)
plt.show()
