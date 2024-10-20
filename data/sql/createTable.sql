CREATE TABLE parkingLot (
    id INT AUTO_INCREMENT PRIMARY KEY,    -- 自增主键
    name VARCHAR(255) NOT NULL,           -- 名称必填
    latitude DECIMAL(16, 12),             -- 纬度，保留12位小数
    longitude DECIMAL(16, 12),            -- 经度，保留12位小数
    createtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，默认当前时间
    updatetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 更新时间，每次更新时自动刷新
);



INSERT INTO parkingLot (name, latitude, longitude)
VALUES ('Central Parking', 37.774929, -122.419418);


drop TABLE parking_occupancy;
drop TABLE ParkingInfo;

CREATE TABLE ParkingInfo (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- 自增主键，必填
    parkingId VARCHAR(50),                   -- 停车位ID，可重复
    plotId VARCHAR(50),                      -- 地块ID，可重复
    occupied TINYINT(1) NOT NULL,            -- 是否占用（0 未占用，1 已占用）
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，默认当前时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 更新时间，随每次更新而更新
);
CREATE TABLE parking_occupancy (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- 自增主键
    plotId INT NOT NULL,                      -- 每个停车位的ID，必填
    num_available INT DEFAULT 0,              -- 占用数量，默认为0
    createtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认为当前时间
    updatatime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 更新时间，每次更新时自动刷新
);

