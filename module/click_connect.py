from functools import partial


def click_connect(main_object):
    # 绑定卡片按钮
    main_object.push_button_60s_news.clicked.connect(main_object.push_button_60s_click)
    main_object.push_button_weibo_info.clicked.connect(main_object.push_button_weibo_click)
    main_object.push_button_looking.clicked.connect(main_object.push_button_looking_click)
    main_object.push_button_reading.clicked.connect(main_object.push_button_reading_click)
    main_object.push_button_todo.clicked.connect(main_object.push_button_todo_click)
    # 城市选择
    main_object.weather_position_label.clicked.connect(main_object.open_city_view)
    # 新增待办事项
    main_object.push_button_todo_add.clicked.connect(partial(main_object.open_new_todo_view, None))
    # 热搜选项按钮
    main_object.push_button_top_weibo.clicked.connect(main_object.push_button_top_weibo_click)
    main_object.push_button_top_baidu.clicked.connect(main_object.push_button_top_baidu_click)
    main_object.push_button_top_bilibili.clicked.connect(main_object.push_button_top_bilibili_click)
    main_object.push_button_top_zhihu.clicked.connect(main_object.push_button_top_zhihu_click)
    main_object.push_button_top_douyin.clicked.connect(main_object.push_button_top_douyin_click)
    main_object.push_button_top_tencent.clicked.connect(main_object.push_button_top_tencent_click)
    # 待办事项按钮
    main_object.push_button_todo_todo.clicked.connect(main_object.push_button_todo_open_click)
    main_object.push_button_todo_ok.clicked.connect(main_object.push_button_todo_close_click)
    # Looking卡片按钮绑定
    main_object.push_button_looking_fish.clicked.connect(main_object.push_button_looking_fish_click)
    main_object.push_button_looking_everyday.clicked.connect(main_object.push_button_looking_everyday_click)
    # main_object.push_button_looking_girl_animation.clicked.connect(main_object.push_button_looking_girl_animation_click)
    # main_object.push_button_looking_girl_real.clicked.connect(main_object.push_button_looking_girl_real_click)
    # Reading卡片按钮绑定
    main_object.push_button_reading_history.clicked.connect(main_object.push_button_reading_history_click)
    main_object.push_button_reading_life.clicked.connect(main_object.push_button_reading_life_click)
    main_object.push_button_reading_riddle.clicked.connect(main_object.push_button_reading_riddle_click)
    main_object.push_button_reading_rainbow.clicked.connect(main_object.push_button_reading_rainbow_click)
    main_object.push_button_reading_morning.clicked.connect(main_object.push_button_reading_morning_click)
    main_object.push_button_reading_night.clicked.connect(main_object.push_button_reading_night_click)
    main_object.push_button_reading_chicken_1.clicked.connect(main_object.push_button_reading_chicken_1_click)
    main_object.push_button_reading_chicken_2.clicked.connect(main_object.push_button_reading_chicken_2_click)
    main_object.push_button_reading_cheesy_love.clicked.connect(main_object.push_button_reading_cheesy_love_click)
    # 喝水绑定
    main_object.label_add.clicked.connect(main_object.push_button_add_click)
    main_object.push_button_restart.clicked.connect(main_object.push_button_clear_click)
    main_object.push_button_drinking_setting.clicked.connect(main_object.open_drinking_setting_view)
    main_object.push_button_drinking_history.clicked.connect(main_object.open_drinking_record_view)
    # 退出
    main_object.push_button_exit.clicked.connect(main_object.quit_before)