# 📂 Kaggle Stable Diffusion 模型与资源添加教程

本脚本支持多种方式添加模型和插件资源。所有的修改均在代码最上方的 **配置区域** 进行。

#### **项目地址：https://www.kaggle.com/code/qq2575044704/stable-diffusion-webui-novelai-edited-version-2**


---

## 方法一：通过 URL 链接下载

脚本会在启动时自动从 Civitai 或 HuggingFace 下载模型。

### 📝 语法格式

请严格遵守以下格式，否则脚本会报错：

```
'文件名.后缀:下载链接',
```

> **注意：**
> 1. 必须包含英文引号 `'`。
> 2. 文件名与链接之间用英文冒号 `:` 隔开。
> 3. 每行末尾必须加英文逗号 `,`。

### 1. 添加大模型（Checkpoint）

找到 `sd_model_urls` 列表：

```python
sd_model_urls=[
    # 格式示例
    '[C站热门]麦橘v6.safetensors:https://civitai.com/api/download/models/94640',
    
    # 添加 ChilloutMix
    'ChilloutMix_Ni.safetensors:https://civitai.com/api/download/models/11745',
]
```

### 2. 添加 LoRA 模型

找到 `lora_model_urls` 列表：

```python
lora_model_urls=[
    # 格式示例
    'AsianCute.safetensors:https://civitai.com/api/download/models/62833',
]
```

---

## 方法二：挂载 Kaggle Dataset（推荐，万能方法）

如果你不想每次启动都消耗时间下载模型，或者有些模型无法下载，可以使用 Kaggle 的 Dataset 功能。

### 📋 操作步骤

1. **添加数据集**：
   - 在 Kaggle 代码编辑页右侧边栏，点击 **`+ Add Input`**。
   - 搜索你需要的模型（如 "Stable Diffusion XL"）。
   - 如果没有，你可以自己上传。自己创建一个数据集。
   - 点击右侧 `+` 号添加。

2. **获取路径**：
   - 添加成功后，右侧 Input 列表中会出现该文件夹。
   - 点击文件夹名称旁边的 **复制图标 (Copy Dataset Path)**。

3. **修改代码**：
   - 找到 **不带 urls 后缀** 的变量（如 `sd_model`），粘贴路径。

4. **图解**
   <img width="1910" height="915" alt="image" src="https://github.com/user-attachments/assets/ee3cd559-8d59-4318-b345-9ef96f4dd585" />

```python
# Stable Diffusion模型数据集路径
sd_model = [
    '/kaggle/input/9527-fp16',
    
    # 粘贴你刚才复制的路径
    "/kaggle/input/你的数据集名称", 
]
```

---

<details>
<summary><strong>🔧 开发者教程 - 添加自定义模型类型与路径（修改源码）</strong></summary>

<br>

如果脚本预设的列表（如 `sd_model`、`lora_model`）无法满足你的需求（例如你需要下载 `Wildcards`、`Adetailer` 或特定插件模型到指定目录），请按照以下两步修改源码。

### 第一步：定义你的链接列表

在代码最上方的 **配置区域**（任意空行处，例如 `lora_model_urls` 下方），创建一个新的列表变量。

```python
# === 在这里定义你的新列表 ===

# 例如：定义 Wildcards (抽卡文件) 的下载列表
wildcards_urls = [
    "rpg_classes.txt:https://civitai.com/api/download/models/12345",
    "https://huggingface.co/username/repo/raw/main/season.txt",
]

# 例如：定义 Adetailer (脸部修复) 的下载列表
adetailer_urls = [
    "face_yolov8n.pt:https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt",
]
```

### 第二步：注册下载任务

按 `Ctrl + F` 搜索函数名：**`def download_model():`**

找到函数内部的 `tasks.extend(...)` 区域，在最后添加你的新任务。

**代码修改位置示例：**

```python
def download_model():
    # ... (前面的代码保持不变) ...
    
    tasks.extend(download_links(animatediff_model_urls, 'animatediffmodel'))
    tasks.extend(download_links(animatediff_lora_urls, 'animatedifflora'))
    
    # =========== 在这里插入你的代码 ===========
    
    # 语法：tasks.extend(download_links(你的列表变量名, f'{install_path}/stable-diffusion-webui/你的目标具体路径'))
    
    # 1. 下载 Wildcards 到插件目录
    tasks.extend(download_links(wildcards_urls, f'{install_path}/stable-diffusion-webui/extensions/sd-dynamic-prompts/wildcards'))
    
    # 2. 下载 Adetailer 模型到模型目录
    tasks.extend(download_links(adetailer_urls, f'{install_path}/stable-diffusion-webui/models/adetailer'))

    # ... (后面的代码保持不变) ...
```

### ✅ 原理说明

该脚本封装了 `download_links(url_list, target_dir)` 函数：

- **参数1**：你在第一步定义的列表变量。
- **参数2**：文件存放的绝对路径。`f'{install_path}/stable-diffusion-webui/...'` 是脚本通用的路径写法。

</details>

---

## ❓ 常见问题排查

| 问题 | 解决方案 |
|------|----------|
| 报错 `SyntaxError: invalid syntax` | 检查列表中每行末尾是否都有逗号 `,`；检查是否误用了中文符号（如 `'` 或 `：`） |
| HuggingFace 下载失败 | 确保链接包含 `/resolve/main/`。如果链接是 `/blob/main/`，请手动修改为 `resolve` |
| Kaggle 空间不足 | 使用方法二（挂载 Dataset）不会占用 `/kaggle/working` 的输出空间，推荐优先使用 |
