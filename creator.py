import os

num_files = 16  # количество файлов

# Папки для разных типов файлов
yaml_dir = 'exercises'
md_dir = 'lessons'

# Создаём папки, если их нет
os.makedirs(yaml_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

# Определяем ширину нумерации
num_width = len(str(num_files))

for i in range(1, num_files + 1):
    num_str = str(i).zfill(num_width)  # например, '01', '02', ...

    # Полные пути к файлам
    md_path = os.path.join(md_dir, f'{num_str}-name.md')
    yaml_path = os.path.join(yaml_dir, f'file_{num_str}-exercises.yaml')

    # Создаём пустые файлы
    open(md_path, 'w').close()
    open(yaml_path, 'w').close()

print(f'Создано {num_files} .md файлов в /{md_dir} и .yaml файлов в /{yaml_dir}')
