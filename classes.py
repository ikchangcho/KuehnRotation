class Person:
    def __init__(self, name, age):  # Self = Instance
        self.name = name            # Attribute
        self.age = age

p1 = Person("John", 25) # Object
print(p1.name)

class Example:
    def __init__(self):
        self.data = []

    def add_item(self, item):
        self.data.append(item)

example = Example()
example.add_item("item1")
example.add_item("item2")
print(example.data)

class CSVDataProcessor:
    def __init__(self, filename_pattern):
        self.filename_pattern = filename_pattern
        self.data = []

    def load_data(self):
        files = sorted(glob.glob(self.filename_pattern))
        for file in files:
            data = pd.read_csv(file).values
            self.data.append(data)

    def choose_x_y(self, init, x_col, x_factor, y_col, y_factor):
        x_y_dydx = []
        for idx, data in enumerate(self.data):
            x = data[init:, x_col] * x_factor
            y = data[init:, y_col] * y_factor
            dy_dx = np.gradient(y, x)  # Derivative
            x_y_dydx.append((x, y, dy_dx))
            df = pd.DataFrame({'x': x, 'y': y, 'dy_dx': dy_dx})
            #df.to_csv(f'x_y_dydx_{idx}.csv', index=False)
        return x_y_dydx

    def plot_data(self, data, xlabel, ylabel, title):
        fig, axs = plt.subplots(len(data), 1, figsize=(8, 6 * len(data)))
        if len(data) == 1:
            axs = [axs]
        for idx, (x, y) in enumerate(data):
            axs[idx].plot(x, y, label=f'Data {idx}')
            axs[idx].set_title(f'{title} {idx}')
            axs[idx].set_xlabel(f'{xlabel}')
            axs[idx].set_ylabel(f'{ylabel}')
            axs[idx].legend()
        plt.tight_layout()
        plt.show()

filename = "/Users/ik/Pycharm/KuehnRotation/260624_1cm2cm_*.csv"

if __name__ == "__main__":
    processor = CSVDataProcessor(f"{filename}")
    processor.load_data()
    processed_data = processor.process_data(2, 3)
    processor.plot_data(processed_data)