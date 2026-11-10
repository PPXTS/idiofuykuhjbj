import flet as ft
import random
import json
import os
import pathlib
import shutil
from pypinyin import lazy_pinyin, Style

# ================= 跨平台安全存储路径（打包手机必备） =================
# 1. 手机上的可读写安全目录 (用于保存你的错题记录等)
data_dir = pathlib.Path(os.getenv("FLET_APP_STORAGE_DATA", "."))
DATA_FILE = data_dir / "server_words.json"

# 2. 动态获取 assets 目录路径 (无论是在电脑上还是手机上，都能精准找到)
assets_dir = pathlib.Path(os.environ.get("FLET_ASSETS_DIR", "assets")).resolve()
SEED_FILE = assets_dir / "server_words.json"

def init_data():
    """首次运行，把打包进去的词库复制到手机的安全目录"""
    if not DATA_FILE.exists():
        try:
            if SEED_FILE.exists():
                shutil.copy(SEED_FILE, DATA_FILE)
            else:
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump([], f)
        except Exception as e:
            print(f"初始化词库异常: {e}")
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

def load_local_words():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"读取数据失败: {e}")
        return []

def save_local_words(words):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"保存数据失败: {e}")

# ================= 🌟 究极狂野版嘴臭/狂夸词库 =================
LOCAL_TAUNTS = {
    "correct": [
        "卧槽，他妈的这你都能对？老子给你磕一个！", 
        "真 tm 牛逼！文曲星附体是吧？这波降维打击，出题人直接被你按在地上摩擦！",
        "这波操作在大气层，牛逼克拉斯，今晚必须加个大鸡腿！",
        "他妈的，脑干突然长出来了？这智商碾压全场啊！",
        "纯纯的神仙下凡，太顶了，这就是传说中的学神吗？",
        "妈的，这波直接封神！连蒙带猜都能对，你开挂了吧！",
        "卧槽，太狠了！直接把出题人底裤都看穿了！",
        "他妈的，这题你都能秒？瞎猫碰上死耗子了吧！",
        "稳如老狗！这波拿捏得死死的，老子给你鼓掌！",
        "牛逼啊！今天状态神勇，是不是吃兴奋剂了？",
        "草，这么难的题都让你装到了，服气！",
        "他妈的，你这知识储备，考官看了都得连夜跑路！"
    ],
    "wrong_1": [
        "瞎了狗眼？这也能选错？妈的！", 
        "他妈的又做错，你脑子是进水了还是进屎了？", 
        "老子闭着眼睛按脚趾头选都比你准！废物！", 
        "长点心吧煞笔，这分丢得你妈都不认识你了！", 
        "纯纯的低级失误，好好看看你选的什么垃圾选项，草！", 
        "他妈的，完美避开所有正确答案，你也是个人才。", 
        "离谱！这选项一看就不对啊，你这眼力见基本告别自行车了。",
        "妈的，选错这种题，你今天出门带脑子了吗？",
        "他妈的，你是不是有选择困难症？瞎jb乱点！",
        "做错这种送分题，你对得起你交的报名费吗？",
        "草，这都能歪，你的直觉跟屎一样。",
        "他妈的，好好的题被你做废了，回炉重造吧！"
    ],
    "wrong_3": [
        "做几遍了还错？记吃不记打是吧，草泥马的！", 
        "你脑仁只有黄豆大吗？这都记不住，不如把脑子捐给火锅店！", 
        "他妈的，这题是你亲爹啊你一直错？属复读机的吗？", 
        "服了，狗改不了吃屎是吧，你这智商基本告别公考了，进厂打螺丝吧！", 
        "再错下去，这词都快认识你了，煞笔！", 
        "妈的，你这记性被狗吃了？这么简单的逻辑想不明白？", 
        "老子真想顺着网线过去给你两巴掌，清醒清醒！",
        "他妈的，你脑子里装的是浆糊还是大肠？完全不用啊！",
        "错错错，就知道错，你是故意来折磨我的吗？",
        "卧槽，你真是个纯纯的小丑，反复踩同一个坑，没救了！",
        "他妈的，我看你是皮痒了欠骂，滚去抄十遍解析！",
        "草，你是不是把脑子忘在娘胎里了？"
    ],
    "wrong_5": [
        "错5次了！你是不是故意来气老子的？草泥马！", 
        "我要是你，早就找个地缝钻进去了，或者直接把手机砸了！", 
        "他妈的，你用脚趾头选的都比这准一万倍，纯纯的废物！", 
        "这智商，建议直接把器官捐给有需要的人，你留着也是浪费氧气！", 
        "草泥马的，脑袋里装的是浆糊吗？无可救药！", 
        "他妈的，你这坨烂泥，糊都糊不上墙，活着就是浪费国家粮食！", 
        "看你做题，简直是对我眼睛的强暴，你这jb脑子还是趁早扔了吧！", 
        "卧槽，你这极品脑残是怎么活到现在的？去死吧！", 
        "妈的，老子真想一脚把你踹回娘胎里重造！", 
        "你这脑回路，连草履虫都嫌弃，真是个纯纯的废物！", 
        "真他妈的是个弱智，这题做错了还理直气壮的？", 
        "草泥马的，赶紧滚去睡觉吧，别在这侮辱公考了！"
    ]
}

def weighted_sample(population, weights, k):
    if len(population) == 0: return []
    k = min(k, len(population))
    selected = []; remaining = list(population); rem_weights = list(weights)
    for _ in range(k):
        total = sum(rem_weights)
        if total <= 0: idx = random.randint(0, len(remaining)-1)
        else:
            r = random.uniform(0, total); s = 0; idx = 0
            for i, w in enumerate(rem_weights):
                s += w
                if s >= r: idx = i; break
        selected.append(remaining[idx]); remaining.pop(idx); rem_weights.pop(idx)
    return selected

def main(page: ft.Page):
    init_data()
    page.title = "词汇特训中枢 (狂野单机版)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#f8fafc"

    current_learning_words, test_questions = [], []

    def show_message(msg, color="#2563eb"):
        page.show_dialog(ft.SnackBar(ft.Text(msg), bgcolor=color))

    def build_appbar(title, back_action):
        return ft.Container(content=ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: back_action()),
            ft.IconButton(icon=ft.Icons.HOME, icon_color="#64748b", tooltip="回首页", on_click=lambda e: show_home()),
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD)
        ]), padding=ft.Padding.only(top=30, left=10, right=10, bottom=10), bgcolor="#f1f5f9")

    # ================= 首页 =================
    def show_home():
        page.controls.clear()
        def big_module_card(title, desc, icon, color, on_click):
            return ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Icon(icon, size=36, color=ft.Colors.WHITE), bgcolor=color, padding=16, border_radius=20),
                    ft.Column([ft.Text(title, size=22, weight=ft.FontWeight.BOLD), ft.Text(desc, size=14, color="#64748b")], spacing=4, expand=True),
                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color="#cbd5e1")
                ]),
                padding=20, bgcolor="#ffffff", border_radius=22, shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK)), ink=True, on_click=on_click
            )
        page.add(ft.Container(content=ft.Column([
            ft.Text("词汇特训中枢", size=36, weight=ft.FontWeight.BOLD),
            ft.Text("完全离线 · 狂野单机版", size=18, color="#64748b"),
            ft.Divider(height=25, color=ft.Colors.TRANSPARENT),
            big_module_card("进入词库", "开始加权刷题、复习错题", ft.Icons.BOOK, "#2563eb", lambda e: show_module_a())
        ], alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.AUTO), padding=25, expand=True))
        page.update()

    # ================= A 模块大厅 =================
    def show_module_a():
        page.controls.clear()
        def module_card(title, desc, icon, on_click):
            return ft.Container(content=ft.Row([ft.Icon(icon, size=40, color="#2563eb"), ft.Column([ft.Text(title, size=20, weight=ft.FontWeight.BOLD), ft.Text(desc, size=14, color="#64748b")], spacing=4, expand=True)]), padding=20, bgcolor="#ffffff", border_radius=22, shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)), ink=True, on_click=on_click)
        page.add(build_appbar("词汇特训", show_home), ft.Container(content=ft.Column([
            module_card("词语辨析", "加权刷题，优先错题", ft.Icons.MENU_BOOK, lambda e: show_learning_setup()),
            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
            module_card("错题本", "复习错题", ft.Icons.BOOKMARK_BORDER, lambda e: show_wrong_book()),
            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
            module_card("词库管理", "查看与编辑词库", ft.Icons.EDIT_NOTE, lambda e: show_manage_list())
        ], alignment=ft.MainAxisAlignment.START), padding=25, expand=True)); page.update()

    # ================= 弹窗查词 =================
    def show_word_popup(word):
        words = load_local_words()
        target = next((w for w in words if w["word"] == word), None)
        
        if not target:
            py_list = lazy_pinyin(word)
            target = {
                "word": word, "pinyin": " ".join(py_list), 
                "meaning": "本地词库暂无该词详细释义，可去【词库管理】补充录入。", 
                "highlight": "", "example": "", "synonyms": [], "antonyms": [], "confusables": []
            }
            
        w = page.width * 0.85 if page.width else 340
        h = page.height * 0.7 if page.height else 500
        card = create_card(target, clickable=False, custom_width=w, custom_height=h)
        dialog = ft.AlertDialog(content=card, content_padding=0, actions=[ft.TextButton("关闭", on_click=lambda e: page.pop_dialog())])
        page.show_dialog(dialog)

    # ================= 学习准备页 =================
    def show_learning_setup():
        page.controls.clear()
        words = load_local_words()
        if not words: show_message("词库为空！请先去词库管理添加。", "#ef4444"); return
        new_words = [w for w in words if w.get("practice_count", 0) == 0]
        old_words = [w for w in words if w.get("practice_count", 0) > 0]
        wrong_words = [w for w in words if w.get("wrong_count", 0) > 0]
        selected_mode = {"type": "mix", "pool": words}
        def mode_card(title, count, type_key, pool):
            def on_click(e): selected_mode["type"] = type_key; selected_mode["pool"] = pool; update_mode_cards()
            return ft.Container(content=ft.Column([ft.Text(title, size=15, weight=ft.FontWeight.BOLD), ft.Text(f"{count} 词", size=13, color="#64748b")], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=16, border_radius=18, bgcolor="#ffffff", expand=True, border=ft.Border.all(2, ft.Colors.TRANSPARENT), on_click=on_click, ink=True)
        card_new = mode_card("新词", len(new_words), "new", new_words); card_old = mode_card("老词", len(old_words), "old", old_words); card_wrong = mode_card("错题", len(wrong_words), "wrong", wrong_words); card_mix = mode_card("混合加权", len(words), "mix", words)
        def update_mode_cards():
            for card in [card_new, card_old, card_wrong, card_mix]: card.border = ft.Border.all(2, ft.Colors.TRANSPARENT)
            if selected_mode["type"] == "new": card_new.border = ft.Border.all(2, "#2563eb")
            elif selected_mode["type"] == "old": card_old.border = ft.Border.all(2, "#2563eb")
            elif selected_mode["type"] == "wrong": card_wrong.border = ft.Border.all(2, "#ef4444")
            else: card_mix.border = ft.Border.all(2, "#2563eb")
            page.update()
        tf_count = ft.TextField(label="题量", value="5", keyboard_type=ft.KeyboardType.NUMBER)
        def start_practice(e):
            pool = selected_mode["pool"]
            if not pool: show_message("该分类没有词汇！", "#ef4444"); return
            try: k = int(tf_count.value); assert k > 0
            except: show_message("请输入有效题量！", "#ef4444"); return
            if selected_mode["type"] == "mix":
                weights = [3 if w.get("wrong_count", 0) > 0 else 1 for w in pool]
                selected_words = weighted_sample(pool, weights, k)
            else: selected_words = random.sample(pool, min(k, len(pool)))
            show_memory_view(selected_words, 0, "词语辨析 - 记忆", show_learning_setup, is_practice=True)
        page.add(build_appbar("词语辨析 - 准备", show_module_a), ft.Container(content=ft.Column([ft.Row([card_new, card_old, card_wrong, card_mix], spacing=8), tf_count, ft.Button("开始练习", on_click=start_practice)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, expand=True)); update_mode_cards()

    # ================= 记忆卡片页 =================
    def show_memory_view(words_list, start_index, title_text, back_func, is_practice=False):
        nonlocal current_learning_words
        if is_practice: current_learning_words = words_list
        current_index = start_index; page.controls.clear()
        page_indicator = ft.Text(f"{current_index + 1} / {len(words_list)}", size=16, color="#64748b", weight=ft.FontWeight.BOLD)
        app_controls = [ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: back_func()), ft.IconButton(icon=ft.Icons.HOME, icon_color="#64748b", on_click=lambda e: show_home()), ft.Text(title_text, size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), page_indicator]
        if is_practice: app_controls.append(ft.Button("进入测试", bgcolor="#22c55e", color=ft.Colors.WHITE, on_click=lambda e: show_finish()))
        app_bar = ft.Container(content=ft.Row(app_controls), padding=ft.Padding.only(top=30, left=10, right=10, bottom=10), bgcolor="#f1f5f9")
        cards_view = ft.PageView(controls=[create_card(w) for w in words_list], expand=True)
        cards_view.selected_index = current_index
        def on_page_change(e):
            nonlocal current_index
            current_index = cards_view.selected_index
            page_indicator.value = f"{current_index + 1} / {len(words_list)}"; page_indicator.update()
            words = load_local_words()
            for w in words:
                if w["word"] == words_list[current_index]["word"]:
                    w["view_count"] = w.get("view_count", 0) + 1
                    break
            save_local_words(words)
        cards_view.on_change = on_page_change
        page.add(app_bar, ft.Container(content=cards_view, expand=True)); page.update()

    # ================= 卡片 UI 渲染 =================
    def build_pinyin_text(pinyin_str, word_str):
        pinyin_list = pinyin_str.split(" "); word_list = list(word_str)
        if len(pinyin_list) == len(word_list):
            cols = [ft.Column([ft.Text(p, size=16, color="#1e293b", weight=ft.FontWeight.W_600), ft.Text(w, size=44, weight=ft.FontWeight.BOLD, color="#1e293b")], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER) for p, w in zip(pinyin_list, word_list)]
            return ft.Row(cols, alignment=ft.MainAxisAlignment.CENTER, spacing=12, wrap=True)
        else: return ft.Column([ft.Text(pinyin_str, size=18, color="#1e293b", weight=ft.FontWeight.W_600), ft.Text(word_str, size=44, weight=ft.FontWeight.BOLD, color="#1e293b")], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)

    def build_example_text(example_str, word_str):
        if word_str in example_str:
            parts = example_str.split(word_str); spans = []
            for i, part in enumerate(parts):
                if part: spans.append(ft.TextSpan(part, style=ft.TextStyle(color="#475569")))
                if i < len(parts) - 1: spans.append(ft.TextSpan(word_str, style=ft.TextStyle(color="#2563eb", weight=ft.FontWeight.BOLD)))
            return ft.Text(spans=spans, size=17, color="#1e293b")
        else: return ft.Text(example_str, size=17, color="#475569")

    def build_relation_card(title, words_list, bg_color, text_color, clickable=True):
        tags = []
        for w in words_list:
            if clickable:
                tags.append(ft.Container(content=ft.Text(w, size=16, color=text_color, weight=ft.FontWeight.W_600), bgcolor="#ffffff", padding=ft.Padding(left=12, right=12, top=6, bottom=6), border_radius=8, on_click=lambda e, word=w: show_word_popup(word), ink=True))
            else:
                tags.append(ft.Container(content=ft.Text(w, size=16, color=text_color, weight=ft.FontWeight.W_600), bgcolor="#ffffff", padding=ft.Padding(left=12, right=12, top=6, bottom=6), border_radius=8))
        return ft.Container(content=ft.Column([ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=text_color), ft.Row(tags, wrap=True, spacing=8, run_spacing=8) if tags else ft.Text("暂无", size=15, color=text_color)], spacing=8), padding=15, bgcolor=bg_color, border_radius=16, expand=True)

    def create_card(data, clickable=True, custom_width=None, custom_height=None):
        wrong, view, count = data.get("wrong_count", 0), data.get("view_count", 0), data.get("practice_count", 0)
        status_tag = ft.Text(f"🔥 错{wrong}次 | 看{view}次", size=14, color="#ef4444", weight=ft.FontWeight.BOLD) if wrong > 0 else ft.Text(f"已练 {count} 次 | 看 {view} 次", size=14, color="#d97706")
        confusables = data.get("confusables", []) or ["暂无"]
        content = ft.Column([
            build_pinyin_text(data.get("pinyin", ""), data["word"]), ft.Row([ft.Container(expand=True), status_tag]), ft.Divider(height=12),
            ft.Row([ft.Text("释义：", size=17, weight=ft.FontWeight.BOLD), ft.Text(data.get("highlight", ""), size=19, weight=ft.FontWeight.BOLD, color="#ef4444"), ft.Text(data.get("meaning", "").replace(data.get("highlight", ""), ""), size=17)], wrap=True),
            ft.Divider(height=24), ft.Text("例句：", size=17, weight=ft.FontWeight.BOLD), build_example_text(data.get("example", ""), data["word"]),
            ft.Divider(height=24), ft.Row([build_relation_card("近义词", data.get("synonyms", []), "#d1fae5", "#065f46", clickable), build_relation_card("反义词", data.get("antonyms", []), "#fee2e2", "#991b1b", clickable)], spacing=12),
            ft.Container(height=8), build_relation_card("易混淆", confusables, "#fef3c7", "#92400e", clickable),
        ], scroll=ft.ScrollMode.AUTO, spacing=12)
        if custom_width: return ft.Container(content=content, padding=30, bgcolor="#ffffff", border_radius=22, width=custom_width, height=custom_height)
        else: return ft.Container(content=content, padding=30, bgcolor="#ffffff", border_radius=22, shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.07, ft.Colors.BLACK)), expand=True)

    # ================= 测试答题页 =================
    def show_finish():
        page.controls.clear()
        def start_test(e): nonlocal test_questions; test_questions = random.sample(current_learning_words, len(current_learning_words)); run_test(0)
        if not current_learning_words: show_message("没有用于测试的词！"); return show_learning_setup()
        page.add(ft.Container(content=ft.Column([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=100, color="#22c55e"), ft.Text("记忆完毕！", size=32, weight=ft.FontWeight.BOLD), ft.Button("开始乱序测试", width=280, bgcolor="#2563eb", color=ft.Colors.WHITE, on_click=start_test), ft.Button("返回上一页", width=280, on_click=lambda e: show_learning_setup())], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=15), alignment=ft.Alignment.CENTER, expand=True)); page.update()

    def run_test(q_index):
        page.controls.clear()
        if q_index >= len(test_questions):
            words = load_local_words()
            for w in words:
                if w["word"] in [tq["word"] for tq in test_questions]:
                    w["practice_count"] = w.get("practice_count", 0) + 1
            save_local_words(words)
            page.add(ft.Container(content=ft.Column([ft.Icon(ft.Icons.EMOJI_EVENTS, size=100, color="#2563eb"), ft.Text("练习完成！", size=32, weight=ft.FontWeight.BOLD), ft.Button("返回模块首页", width=280, bgcolor="#2563eb", color=ft.Colors.WHITE, on_click=lambda e: show_learning_setup())], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=15), alignment=ft.Alignment.CENTER, expand=True)); page.update(); return
        
        current_q = test_questions[q_index]
        options_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
        result_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, visible=False); next_btn = ft.Button("下一题", width=320, height=50, bgcolor="#2563eb", color=ft.Colors.WHITE, visible=False)
        wrong_count = current_q.get("wrong_count", 0)
        
        quiz_content = ft.Column([
            ft.Row([ft.Text(f"进度: {q_index + 1}/{len(test_questions)}", size=16, color="#64748b", weight=ft.FontWeight.BOLD), ft.Text(f"🔥 错 {wrong_count} 次" if wrong_count > 0 else "✨ 新词挑战", size=16, color="#ef4444" if wrong_count > 0 else "#64748b", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Container(content=ft.Column([ft.Text(current_q["word"], size=52, weight=ft.FontWeight.BOLD, color="#1e293b"), ft.Text("请选择正确的释义：", size=18, color="#64748b"), ft.Divider(height=30, color=ft.Colors.TRANSPARENT), options_column, ft.Divider(height=20, color=ft.Colors.TRANSPARENT), result_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO), expand=True, alignment=ft.Alignment.TOP_CENTER),
            ft.Container(content=next_btn, alignment=ft.Alignment.CENTER, padding=ft.Padding.only(bottom=20))
        ], expand=True)
        page.add(build_appbar("乱序测试", show_learning_setup), ft.Container(content=quiz_content, padding=ft.Padding.only(left=30, right=30, top=10, bottom=10), expand=True)); page.update()
        
        def fetch_options():
            all_words = load_local_words()
            distractors = []
            for w in all_words:
                if w["word"] != current_q["word"] and w["meaning"] != current_q["meaning"]:
                    distractors.append(w["meaning"])
            
            random.shuffle(distractors)
            final_opts = [current_q["meaning"]]
            for d in distractors:
                if d not in final_opts:
                    final_opts.append(d)
                if len(final_opts) == 3: break
            
            while len(final_opts) < 3: final_opts.append("无关选项")
            random.shuffle(final_opts)
            
            option_buttons = []
            def check_answer(e, selected_text, btn):
                is_correct = (selected_text == current_q["meaning"])
                for b in option_buttons: b.disabled = True
                
                if not is_correct:
                    words = load_local_words()
                    for w in words:
                        if w["word"] == current_q["word"]:
                            w["wrong_count"] = w.get("wrong_count", 0) + 1
                            new_wc = w["wrong_count"]
                            break
                    save_local_words(words)
                    
                    if new_wc >= 5: taunt = random.choice(LOCAL_TAUNTS["wrong_5"])
                    elif new_wc >= 3: taunt = random.choice(LOCAL_TAUNTS["wrong_3"])
                    else: taunt = random.choice(LOCAL_TAUNTS["wrong_1"])
                    
                    btn.bgcolor = "#fecdd3"
                    result_text.value = f"❌ 错了！正确答案是：{current_q['meaning']}\n\n💬 {taunt}"
                else:
                    taunt = random.choice(LOCAL_TAUNTS["correct"])
                    btn.bgcolor = "#d1fae5"
                    result_text.value = f"✅ 答对了！\n\n💬 {taunt}"
                    
                result_text.visible = True; next_btn.visible = True; page.update()

            for opt in final_opts:
                btn = ft.Button(content=ft.Text(opt, size=16, no_wrap=False), width=500, height=50)
                btn.on_click = lambda e, o=opt, b=btn: check_answer(e, o, b); option_buttons.append(btn)
            options_column.controls = option_buttons; page.update()
            
        next_btn.on_click = lambda e: run_test(q_index + 1)
        page.run_thread(fetch_options)

    # ================= 错题本 =================
    def show_wrong_book():
        page.controls.clear()
        words = load_local_words(); wrong_words = [w for w in words if w.get("wrong_count", 0) > 0]
        search_field = ft.TextField(hint_text="搜索错题", prefix_icon=ft.Icons.SEARCH, content_padding=14, border_radius=16, bgcolor="#ffffff")
        list_view = ft.ListView(expand=True, spacing=12)
        def render_list(e=None):
            list_view.controls.clear()
            if not wrong_words:
                list_view.controls.append(ft.Container(content=ft.Column([ft.Icon(ft.Icons.CHECK_CIRCLE, size=70, color="#22c55e"), ft.Text("太棒了，目前没有错题！", size=20, color="#64748b")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.Alignment.CENTER, padding=60)); page.update(); return
            query = search_field.value.strip() if search_field.value else ""
            display_list = [w for w in wrong_words if query in w["word"]] if query else wrong_words
            grouped_words = {}
            for w in display_list:
                first_letter = lazy_pinyin(w["word"], style=Style.FIRST_LETTER)[0].upper()
                if not ('A' <= first_letter <= 'Z'): first_letter = "#"
                if first_letter not in grouped_words: grouped_words[first_letter] = []
                grouped_words[first_letter].append(w)
            sorted_letters = sorted([k for k in grouped_words.keys() if k != "#"])
            if "#" in grouped_words: sorted_letters.append("#")
            for letter in sorted_letters:
                list_view.controls.append(ft.Container(content=ft.Text(letter, size=20, weight=ft.FontWeight.BOLD, color="#2563eb"), margin=ft.Margin.only(top=14, bottom=8, left=8)))
                for idx, w in enumerate(grouped_words[letter]): list_view.controls.append(create_word_item(w, grouped_words[letter], idx))
            page.update()
        def create_word_item(w, current_global_list, index_in_global):
            def remove_item(e):
                words = load_local_words()
                for word in words:
                    if word["word"] == w["word"]:
                        word["wrong_count"] = 0
                        break
                save_local_words(words)
                show_message("已移出错题本！", "#22c55e"); show_wrong_book()
            return ft.Container(content=ft.Row([ft.Column([ft.Text(w["word"], size=18, weight=ft.FontWeight.BOLD), ft.Text(f"累计错 {w['wrong_count']} 次", size=14, color="#ef4444")], spacing=4), ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color="#ef4444", on_click=remove_item)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=16, bgcolor="#ffffff", border_radius=18, on_click=lambda e, lst=current_global_list, idx=index_in_global: show_memory_view(lst, idx, "错题复习", show_wrong_book), ink=True)
        search_field.on_change = render_list
        page.add(build_appbar("错题本", show_module_a), ft.Container(content=ft.Column([search_field, ft.Divider(height=14, color=ft.Colors.TRANSPARENT), list_view]), padding=ft.Padding.only(left=20, right=20, bottom=20), expand=True))
        render_list()

    # ================= 词库管理 =================
    def show_manage_list():
        page.controls.clear()
        words_cache = load_local_words()
        stats_text = ft.Text(f"词库总览：共 {len(words_cache)} 个词", size=15, color="#2563eb", weight=ft.FontWeight.BOLD)
        search_field = ft.TextField(hint_text="搜索词库", prefix_icon=ft.Icons.SEARCH, content_padding=14, border_radius=16, bgcolor="#ffffff")
        list_view = ft.ListView(expand=True, spacing=12)
        def render_list(e=None):
            list_view.controls.clear()
            if not words_cache:
                list_view.controls.append(ft.Text("云端词库为空！", color="#64748b", size=18)); page.update(); return
            query = search_field.value.strip() if search_field.value else ""
            display_list = [w for w in words_cache if query in w["word"]] if query else words_cache
            grouped_words = {}
            for w in display_list:
                first_letter = lazy_pinyin(w["word"], style=Style.FIRST_LETTER)[0].upper()
                if not ('A' <= first_letter <= 'Z'): first_letter = "#"
                if first_letter not in grouped_words: grouped_words[first_letter] = []
                grouped_words[first_letter].append(w)
            sorted_letters = sorted([k for k in grouped_words.keys() if k != "#"])
            if "#" in grouped_words: sorted_letters.append("#")
            for letter in sorted_letters:
                list_view.controls.append(ft.Container(content=ft.Text(letter, size=20, weight=ft.FontWeight.BOLD, color="#2563eb"), margin=ft.Margin.only(top=14, bottom=8, left=8)))
                for idx, w in enumerate(grouped_words[letter]): list_view.controls.append(create_word_item(w, grouped_words[letter], idx))
            page.update()
        def create_word_item(w, current_global_list, index_in_global):
            def delete_word(e):
                words = load_local_words()
                words = [word for word in words if word["word"] != w["word"]]
                save_local_words(words)
                show_message("删除成功", "#22c55e"); show_manage_list()
            return ft.Container(content=ft.Row([ft.Column([ft.Text(w["word"], size=18, weight=ft.FontWeight.BOLD), ft.Text(f"练习次数：{w.get('practice_count', 0)}", size=14, color="#64748b")], spacing=4), ft.Row([ft.IconButton(icon=ft.Icons.EDIT, icon_color="#2563eb", on_click=lambda e, data=w: edit_word_form(data)), ft.IconButton(icon=ft.Icons.DELETE, icon_color="#ef4444", on_click=delete_word)])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=16, bgcolor="#ffffff", border_radius=18, on_click=lambda e, lst=current_global_list, idx=index_in_global: show_memory_view(lst, idx, "词库浏览", show_manage_list), ink=True)
        search_field.on_change = render_list
        app_bar = ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: show_module_a()), ft.IconButton(icon=ft.Icons.HOME, icon_color="#64748b", on_click=lambda e: show_home()), ft.Text("词库管理", size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), ft.IconButton(icon=ft.Icons.ADD, icon_color="#22c55e", icon_size=30, on_click=lambda e: edit_word_form(None))]), padding=ft.Padding.only(top=30, left=10, right=10, bottom=10), bgcolor="#f1f5f9")
        page.add(app_bar, ft.Container(content=ft.Column([stats_text, search_field, ft.Divider(height=14, color=ft.Colors.TRANSPARENT), list_view], spacing=12), padding=ft.Padding.only(left=20, right=20, bottom=20), expand=True))
        render_list()

    def edit_word_form(data):
        page.controls.clear()
        is_new = (data is None)
        if is_new: data = {"word": "", "pinyin": "", "meaning": "", "highlight": "", "example": "", "synonyms": [], "antonyms": [], "confusables": [], "practice_count": 0, "wrong_count": 0, "view_count": 0}
        tf_word = ft.TextField(label="词语/成语", value=data["word"], border_radius=16)
        tf_pinyin = ft.TextField(label="拼音", value=data["pinyin"], border_radius=16)
        tf_meaning = ft.TextField(label="完整释义", value=data["meaning"], multiline=True, border_radius=16)
        tf_highlight = ft.TextField(label="重点高亮词", value=data["highlight"], border_radius=16)
        tf_example = ft.TextField(label="例句", value=data["example"], multiline=True, border_radius=16)
        tf_syn = ft.TextField(label="近义词", value=",".join(data.get("synonyms", [])), border_radius=16)
        tf_ant = ft.TextField(label="反义词", value=",".join(data.get("antonyms", [])), border_radius=16)
        tf_conf = ft.TextField(label="易混淆词", value=",".join(data.get("confusables", [])), border_radius=16)
        
        def auto_fill(e):
            word = tf_word.value.strip()
            if not word: return show_message("请先输入词语！", "#ef4444")
            py_list = lazy_pinyin(word)
            tf_pinyin.value = " ".join(py_list)
            words = load_local_words()
            target = next((w for w in words if w["word"].strip() == word), None)
            if target:
                tf_meaning.value = target.get("meaning", "")
                tf_highlight.value = target.get("highlight", "")
                tf_example.value = target.get("example", "")
                tf_syn.value = ",".join(target.get("synonyms", []))
                tf_ant.value = ",".join(target.get("antonyms", []))
                tf_conf.value = ",".join(target.get("confusables", []))
                show_message("✅ 已从本地词库补全数据！", "#22c55e")
            else:
                show_message("✨ 拼音已生成。本地未找到详细释义，请手动填写。", "#f97316")
            page.update()
            
        def save_word(e):
            if not tf_word.value.strip(): return show_message("词语不能为空！", "#ef4444")
            new_data = {"word": tf_word.value.strip(), "pinyin": tf_pinyin.value.strip(), "meaning": tf_meaning.value.strip(), "highlight": tf_highlight.value.strip(), "example": tf_example.value.strip(), "synonyms": [x.strip() for x in tf_syn.value.replace("，", ",").split(",") if x.strip()], "antonyms": [x.strip() for x in tf_ant.value.replace("，", ",").split(",") if x.strip()], "confusables": [x.strip() for x in tf_conf.value.replace("，", ",").split(",") if x.strip()], "practice_count": data.get("practice_count", 0), "wrong_count": data.get("wrong_count", 0), "view_count": data.get("view_count", 0)}
            
            words = load_local_words()
            existing_idx = next((i for i, w in enumerate(words) if w["word"].strip() == new_data["word"]), -1)
            if existing_idx >= 0:
                new_data["practice_count"] = words[existing_idx].get("practice_count", 0)
                new_data["wrong_count"] = words[existing_idx].get("wrong_count", 0)
                new_data["view_count"] = words[existing_idx].get("view_count", 0)
                words[existing_idx] = new_data
                show_message("✅ 已更新现有词汇！", "#22c55e")
            else:
                words.append(new_data)
                show_message("✅ 新增词汇成功！", "#22c55e")
                
            save_local_words(words)
            show_manage_list()
            
        app_bar = ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: show_manage_list()), ft.IconButton(icon=ft.Icons.HOME, icon_color="#64748b", on_click=lambda e: show_home()), ft.Text("新增" if is_new else "修改", size=20, weight=ft.FontWeight.BOLD), ft.IconButton(icon=ft.Icons.SAVE, icon_color="#2563eb", on_click=save_word)]), padding=ft.Padding.only(top=30, left=10, right=10, bottom=10), bgcolor="#f1f5f9")
        page.add(app_bar, ft.Container(content=ft.Column([ft.Row([ft.Container(content=tf_word, expand=True), ft.IconButton(icon=ft.Icons.AUTO_AWESOME, icon_color="#f97316", icon_size=30, tooltip="本地生成拼音/查找词库", on_click=auto_fill)]), tf_pinyin, tf_meaning, tf_highlight, tf_example, tf_syn, tf_ant, tf_conf, ft.Container(height=14), ft.Button("保存至本地", width=300, bgcolor="#2563eb", color=ft.Colors.WHITE, on_click=save_word)], spacing=16, scroll=ft.ScrollMode.AUTO), padding=20, expand=True)); page.update()

    show_home()

ft.run(main)