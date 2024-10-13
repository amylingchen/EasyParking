const carImageUrl = 'static/image/car.jpg'; // 替换为实际的汽车图片URL
const gridContainer = document.getElementById('grid-container');

// 创建100个网格单元
for (let i = 0; i < 100; i++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');

    const img = document.createElement('img');
    img.src = carImageUrl;
    img.alt = '汽车图片';
    img.classList.add('car-image');
    cell.appendChild(img);
    gridContainer.appendChild(cell);
}

