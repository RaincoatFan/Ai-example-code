import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 480)
# 刷新的帧率
FRAME_PER_SEC = 60


class PlaneGame(object):
    def __init__(self):
        print("界面初始化")
        # 加载相应的图片
        self.row, self.col = eval(input("请输入环境空间的行列数： "))
        self.dirt = pygame.image.load('./dirt.png')
        self.vacuum = pygame.image.load('./vacuum.png')
        self.block = pygame.image.load('./block.png')
        self.cell_width = 10
        self.cell_height = 10
        # 创建窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("吸尘器的任务环境")
        # 创建时钟
        self.clock = pygame.time.Clock()
        # 存储有垃圾的网格位置
        self.dirt_add = []
        # 存储吸尘器的初始位置并记录吸尘器的运动路径
        self.vacuum_add = None
        # 存储有障碍的网格位置
        self.block_add = []
        self.dirt_vec = []
        self.block_vec = []

    def start_game(self):
        print("开启界面...")
        while True:
            self.draw_background(self.row, self.col)
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            if len(self.dirt_add) > 0:
                for point in self.dirt_add:
                    self.screen.blit(self.dirt, point)
            if len(self.block_add) > 0:
                for point in self.block_add:
                    self.screen.blit(self.block, point)
            if self.vacuum_add != None:
                self.screen.blit(self.vacuum, self.vacuum_add)

            # 更新显示
            pygame.display.update()

    def draw_background(self, row, col):
        self.screen.fill((255, 255, 255))
        WIDTH = SCREEN_RECT.size[0]
        HEIGHT = SCREEN_RECT.size[1]
        self.cell_width = WIDTH / col
        self.cell_height = HEIGHT / row
        # 将对应的图片进行方格大小的尺度缩放
        self.dirt = pygame.transform.scale(self.dirt, (int(self.cell_width), int(self.cell_height)))
        self.vacuum = pygame.transform.scale(self.vacuum, (int(self.cell_width), int(self.cell_height)))
        self.block = pygame.transform.scale(self.block, (int(self.cell_width), int(self.cell_height)))
        # 绘制行
        for r in range(row):
            pygame.draw.line(self.screen, (0, 0, 0), (0, r * self.cell_height),
                             (WIDTH, r * self.cell_height))
        # 绘制列
        for c in range(col):
            pygame.draw.line(self.screen, (0, 0, 0), (c * self.cell_width, 0),
                             (c * self.cell_width, HEIGHT))

    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否退出界面
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0] // self.cell_width
                y = event.pos[1] // self.cell_height
                if event.button == 1:
                    print(event)
                    print("在{},{}放置了一堆垃圾".format(x, y))
                    self.dirt_add.append((x * self.cell_width, y * self.cell_height))
                    self.dirt_vec.append((x, y))
                    print(self.dirt_vec)
                elif event.button == 3:
                    print(event)
                    print("在{},{}放置了一个障碍".format(x, y))
                    self.block_add.append((x * self.cell_width, y * self.cell_height))
                    self.block_vec.append((x, y))
                    print(self.block_vec)
                elif event.button == 2 or event.button == 4 or event.button == 5:
                    print(event)
                    print("在{},{}放置了一个扫地机器人".format(x, y))
                    self.vacuum_add = (x * self.cell_width, y * self.cell_height)

    def __game_over():
        print("关闭界面")
        pygame.quit()
        exit()


if __name__ == "__main__":
    # 创建对象
    game = PlaneGame()
    # 启动界面
    game.start_game()