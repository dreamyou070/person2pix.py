import os
import re
import toml
import shutil
import zipfile
from time import time
from IPython.display import Markdown, display

# These carry information from past executions
if "model_url" in globals():
    old_model_url = model_url
else:
    old_model_url = None
if "dependencies_installed" not in globals():
    dependencies_installed = False
if "model_file" not in globals():
    model_file = None

# These may be set by other cells, some are legacy
if "custom_dataset" not in globals():
    custom_dataset = None
if "override_dataset_config_file" not in globals():
    override_dataset_config_file = None
if "override_config_file" not in globals():
    override_config_file = None
if "optimizer" not in globals():
    optimizer = "AdamW8bit"
if "optimizer_args" not in globals():
    optimizer_args = None
if "continue_from_lora" not in globals():
    continue_from_lora = ""
if "weighted_captions" not in globals():
    weighted_captions = False
if "adjust_tags" not in globals():
    adjust_tags = False
if "keep_tokens_weight" not in globals():
    keep_tokens_weight = 1.0

COLAB = True  # low ram
COMMIT = "5050971ac687dca70ba0486a583d283e8ae324e2"
BETTER_EPOCH_NAMES = True
LOAD_TRUNCATED_IMAGES = True

# @title ## 🚩 Start Here

# @markdown ### ▶️ Setup
# @markdown Your project name will be the same as the folder containing your images. Spaces aren't allowed.
project_name = ""  # @param {type:"string"}
# @markdown The folder structure doesn't matter and is purely for comfort. Make sure to always pick the same one. I like organizing by project.
folder_structure = "Organize by project (MyDrive/Loras/project_name/dataset)"  # @param ["Organize by category (MyDrive/lora_training/datasets/project_name)", "Organize by project (MyDrive/Loras/project_name/dataset)"]
# @markdown Decide the model that will be downloaded and used for training. These options should produce clean and consistent results. You can also choose your own by pasting its download link.
training_model = "Anime (animefull-final-pruned-fp16.safetensors)"  # @param ["Anime (animefull-final-pruned-fp16.safetensors)", "AnyLora (AnyLoRA_noVae_fp16-pruned.ckpt)", "Stable Diffusion (sd-v1-5-pruned-noema-fp16.safetensors)"]
optional_custom_training_model_url = ""  # @param {type:"string"}
custom_model_is_based_on_sd2 = False  # @param {type:"boolean"}

if optional_custom_training_model_url:
    model_url = optional_custom_training_model_url
elif "AnyLora" in training_model:
    model_url = "https://huggingface.co/Lykon/AnyLoRA/resolve/main/AnyLoRA_noVae_fp16-pruned.ckpt"
elif "Anime" in training_model:
    model_url = "https://huggingface.co/hollowstrawberry/stable-diffusion-guide/resolve/main/models/animefull-final-pruned-fp16.safetensors"
else:
    model_url = "https://huggingface.co/hollowstrawberry/stable-diffusion-guide/resolve/main/models/sd-v1-5-pruned-noema-fp16.safetensors"

# @markdown ### ▶️ Processing
# @markdown Resolution of 512 is standard for Stable Diffusion 1.5. Higher resolution training is much slower but can lead to better details. <p>
# @markdown Images will be automatically scaled while training to produce the best results, so you don't need to crop or resize anything yourself.
resolution = 512  # @param {type:"slider", min:512, max:1024, step:128}
# @markdown This option will train your images both normally and flipped, for no extra cost, to learn more from them. Turn it on specially if you have less than 20 images. <p> 
# @markdown **Turn it off if you care about asymmetrical elements in your Lora**.
flip_aug = False  # @param {type:"boolean"}
# markdown Leave empty for no captions.
caption_extension = ".txt"  # param {type:"string"}
# @markdown Shuffling anime tags in place improves learning and prompting. An activation tag goes at the start of every text file and will not be shuffled.
shuffle_tags = True  # @param {type:"boolean"}
shuffle_caption = shuffle_tags
activation_tags = "1"  # @param [0,1,2,3]
keep_tokens = int(activation_tags)

# @markdown ### ▶️ Steps <p>
# @markdown Your images will repeat this number of times during training. I recommend that your images multiplied by their repeats is between 200 and 400.
num_repeats = 10  # @param {type:"number"}
# @markdown Choose how long you want to train for. A good starting point is around 10 epochs or around 2000 steps.<p>
# @markdown One epoch is a number of steps equal to: your number of images multiplied by their repeats, divided by batch size. <p>
preferred_unit = "Epochs"  # @param ["Epochs", "Steps"]
how_many = 10  # @param {type:"number"}
max_train_epochs = how_many if preferred_unit == "Epochs" else None
max_train_steps = how_many if preferred_unit == "Steps" else None
# @markdown Saving more epochs will let you compare your Lora's progress better.
save_every_n_epochs = 1  # @param {type:"number"}
keep_only_last_n_epochs = 10  # @param {type:"number"}
if not save_every_n_epochs:
    save_every_n_epochs = max_train_epochs
if not keep_only_last_n_epochs:
    keep_only_last_n_epochs = max_train_epochs
# @markdown Increasing the batch size makes training faster, but may make learning worse. Recommended 2 or 3.
train_batch_size = 2  # @param {type:"slider", min:1, max:8, step:1}

# @markdown ### ▶️ Learning
# @markdown The learning rate is the most important for your results. If you want to train slower with lots of images, or if your dim and alpha are high, move the unet to 2e-4 or lower. <p>
# @markdown The text encoder helps your Lora learn concepts slightly better. It is recommended to make it half or a fifth of the unet. If you're training a style you can even set it to 0.
unet_lr = 5e-4  # @param {type:"number"}
text_encoder_lr = 1e-4  # @param {type:"number"}
# @markdown The scheduler is the algorithm that guides the learning rate. If you're not sure, pick `constant` and ignore the number. I personally recommend `cosine_with_restarts` with 3 restarts.
lr_scheduler = "cosine_with_restarts"  # @param ["constant", "cosine", "cosine_with_restarts", "constant_with_warmup", "linear", "polynomial"]
lr_scheduler_number = 3  # @param {type:"number"}
lr_scheduler_num_cycles = lr_scheduler_number if lr_scheduler == "cosine_with_restarts" else 0
lr_scheduler_power = lr_scheduler_number if lr_scheduler == "polynomial" else 0
# @markdown Steps spent "warming up" the learning rate during training for efficiency. I recommend leaving it at 5%.
lr_warmup_ratio = 0.05  # @param {type:"slider", min:0.0, max:0.5, step:0.01}
lr_warmup_steps = 0
# @markdown New feature that adjusts loss over time, makes learning much more efficient, and training can be done with about half as many epochs. Uses a value of 5.0 as recommended by [the paper](https://arxiv.org/abs/2303.09556).
min_snr_gamma = True  # @param {type:"boolean"}
min_snr_gamma_value = 5.0 if min_snr_gamma else None

# @markdown ### ▶️ Structure
# @markdown LoRA is the classic type, while LoCon is good with styles. Lycoris require [this extension](https://github.com/KohakuBlueleaf/a1111-sd-webui-lycoris) for webui to work like normal loras. More info [here](https://github.com/KohakuBlueleaf/Lycoris).
lora_type = "LoRA"  # @param ["LoRA", "LoCon Lycoris", "LoHa Lycoris"]

# @markdown Below are some recommended values for the following settings:

# @markdown | type | network_dim | network_alpha | conv_dim | conv_alpha |
# @markdown | :---: | :---: | :---: | :---: | :---: |
# @markdown | LoRA | 32 | 16 |   |   |
# @markdown | LoCon | 16 | 8 | 8 | 1 |
# @markdown | LoHa | 8 | 4 | 4 | 1 |

# @markdown More dim means larger Lora, it can hold more information but more isn't always better. A dim between 8-32 is recommended, and alpha equal to half the dim.
network_dim = 16  # @param {type:"slider", min:1, max:128, step:1}
network_alpha = 8  # @param {type:"slider", min:1, max:128, step:1}
# @markdown The following values don't affect LoRA. They work like dim/alpha but only for the additional learning layers of Lycoris.
conv_dim = 8  # @param {type:"slider", min:1, max:64, step:1}
conv_alpha = 1  # @param {type:"slider", min:1, max:64, step:1}
conv_compression = False  # @param {type:"boolean"}

network_module = "lycoris.kohya" if "Lycoris" in lora_type else "networks.lora"
network_args = None if lora_type == "LoRA" else [
    f"conv_dim={conv_dim}",
    f"conv_alpha={conv_alpha}",
]
if "Lycoris" in lora_type:
    network_args.append(f"algo={'loha' if 'LoHa' in lora_type else 'lora'}")
    network_args.append(f"disable_conv_cp={str(not conv_compression)}")

# markdown ### ▶️ Experimental
# markdown Save additional data equaling ~1 GB allowing you to resume training later.
save_state = False  # param {type:"boolean"}
# markdown Resume training if a save state is found.
resume = False  # param {type:"boolean"}

# @markdown ### ▶️ Ready
# @markdown You can now run this cell to cook your Lora. Good luck! <p>


# 👩‍💻 Cool code goes here

if optimizer == "DAdaptation":
    optimizer_args = ["decouple=True", "weight_decay=0.02", "betas=[0.9,0.99]"]
    unet_lr = 0.5
    text_encoder_lr = 0.5
    lr_scheduler = "constant_with_warmup"
    network_alpha = network_dim

root_dir = "/content" if COLAB else "~/Loras"
deps_dir = os.path.join(root_dir, "deps")
repo_dir = os.path.join(root_dir, "kohya-trainer")

if "/Loras" in folder_structure:
    main_dir = os.path.join(root_dir, "drive/MyDrive/Loras") if COLAB else root_dir
    log_folder = os.path.join(main_dir, "_logs")
    config_folder = os.path.join(main_dir, project_name)
    images_folder = os.path.join(main_dir, project_name, "dataset")
    output_folder = os.path.join(main_dir, project_name, "output")
else:
    main_dir = os.path.join(root_dir, "drive/MyDrive/lora_training") if COLAB else root_dir
    images_folder = os.path.join(main_dir, "datasets", project_name)
    output_folder = os.path.join(main_dir, "output", project_name)
    config_folder = os.path.join(main_dir, "config", project_name)
    log_folder = os.path.join(main_dir, "log")

config_file = os.path.join(config_folder, "training_config.toml")
dataset_config_file = os.path.join(config_folder, "dataset_config.toml")
accelerate_config_file = os.path.join(repo_dir, "accelerate_config/config.yaml")


def clone_repo():
    os.chdir(root_dir)
    !git
    clone
    https: // github.com / kohya - ss / sd - scripts
    {repo_dir}
    os.chdir(repo_dir)
    if COMMIT:
        !git
        reset - -hard
        {COMMIT}
    !wget
    https: // raw.githubusercontent.com / hollowstrawberry / kohya - colab / main / requirements.txt - q - O
    requirements.txt


def install_dependencies():
    clone_repo()
    !apt - y
    update - qq
    !apt - y
    install
    aria2
    !pip - q
    install - -upgrade - r
    requirements.txt - -extra - index - url
    https: // download.pytorch.org / whl / cu118

    # patch kohya for minor stuff
    if COLAB:
        !sed - i
        "s@cpu@cuda@"
        library / model_util.py  # low ram
    if LOAD_TRUNCATED_IMAGES:
        !sed - i
        's/from PIL import Image/from PIL import Image, ImageFile\nImageFile.LOAD_TRUNCATED_IMAGES=True/g'
        library / train_util.py  # fix truncated jpegs error
    if BETTER_EPOCH_NAMES:
        !sed - i
        's/{:06d}/{:02d}/g'
        library / train_util.py  # make epoch names shorter
        !sed - i
        's/model_name + "."/model_name + "-{:02d}.".format(num_train_epochs)/g'
        train_network.py  # name of the last epoch will match the rest

    from accelerate.utils import write_basic_config
    if not os.path.exists(accelerate_config_file):
        write_basic_config(save_location=accelerate_config_file)

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    os.environ["BITSANDBYTES_NOWELCOME"] = "1"
    os.environ["SAFETENSORS_FAST_GPU"] = "1"


def validate_dataset():
    global lr_warmup_steps, lr_warmup_ratio, caption_extension, keep_tokens, keep_tokens_weight, weighted_captions, adjust_tags
    supported_types = (".png", ".jpg", ".jpeg")

    print("\n💿 Checking dataset...")
    if not project_name.strip() or any(c in project_name for c in " .()\"'\\/"):
        print("💥 Error: Please choose a valid project name.")
        return

    if custom_dataset:
        try:
            datconf = toml.loads(custom_dataset)
            datasets = [d for d in datconf["datasets"][0]["subsets"]]
        except:
            print(f"💥 Error: Your custom dataset is invalid or contains an error! Please check the original template.")
            return
        reg = [d for d in datasets if d.get("is_reg", False)]
        for r in reg:
            print("📁" + r["image_dir"].replace("/content/drive/", "") + " (Regularization)")
        datasets = [d for d in datasets if d not in reg]
        datasets_dict = {d["image_dir"]: d["num_repeats"] for d in datasets}
        folders = datasets_dict.keys()
        files = [f for folder in folders for f in os.listdir(folder)]
        images_repeats = {
            folder: (len([f for f in os.listdir(folder) if f.lower().endswith(supported_types)]), datasets_dict[folder])
            for folder in folders}
    else:
        folders = [images_folder]
        files = os.listdir(images_folder)
        images_repeats = {images_folder: (len([f for f in files if f.lower().endswith(supported_types)]), num_repeats)}

    for folder in folders:
        if not os.path.exists(folder):
            print(f"💥 Error: The folder {folder.replace('/content/drive/', '')} doesn't exist.")
            return
    for folder, (img, rep) in images_repeats.items():
        if not img:
            print(f"💥 Error: Your {folder.replace('/content/drive/', '')} folder is empty.")
            return
    for f in files:
        if not f.lower().endswith(".txt") and not f.lower().endswith(supported_types):
            print(f"💥 Error: Invalid file in dataset: \"{f}\". Aborting.")
            return

    if not [txt for txt in files if txt.lower().endswith(".txt")]:
        caption_extension = ""
    if continue_from_lora and not (continue_from_lora.endswith(".safetensors") and os.path.exists(continue_from_lora)):
        print(f"💥 Error: Invalid path to existing Lora. Example: /content/drive/MyDrive/Loras/example.safetensors")
        return

    pre_steps_per_epoch = sum(img * rep for (img, rep) in images_repeats.values())
    steps_per_epoch = pre_steps_per_epoch / train_batch_size
    total_steps = max_train_steps or int(max_train_epochs * steps_per_epoch)
    estimated_epochs = int(total_steps / steps_per_epoch)
    lr_warmup_steps = int(total_steps * lr_warmup_ratio)

    for folder, (img, rep) in images_repeats.items():
        print("📁" + folder.replace("/content/drive/", ""))
        print(f"📈 Found {img} images with {rep} repeats, equaling {img * rep} steps.")
    print(
        f"📉 Divide {pre_steps_per_epoch} steps by {train_batch_size} batch size to get {steps_per_epoch} steps per epoch.")
    if max_train_epochs:
        print(f"🔮 There will be {max_train_epochs} epochs, for around {total_steps} total training steps.")
    else:
        print(f"🔮 There will be {total_steps} steps, divided into {estimated_epochs} epochs and then some.")

    if total_steps > 10000:
        print("💥 Error: Your total steps are too high. You probably made a mistake. Aborting...")
        return

    if adjust_tags:
        print(f"\n📎 Weighted tags: {'ON' if weighted_captions else 'OFF'}")
        if weighted_captions:
            print(f"📎 Will use {keep_tokens_weight} weight on {keep_tokens} activation tag(s)")
        print("📎 Adjusting tags...")
        adjust_weighted_tags(folders, keep_tokens, keep_tokens_weight, weighted_captions)

    return True


def adjust_weighted_tags(folders, keep_tokens: int, keep_tokens_weight: float, weighted_captions: bool):
    weighted_tag = re.compile(r"\((.+?):[.\d]+\)(,|$)")
    for folder in folders:
        for txt in [f for f in os.listdir(folder) if f.lower().endswith(".txt")]:
            with open(os.path.join(folder, txt), 'r') as f:
                content = f.read()
            # reset previous changes
            content = content.replace('\\', '')
            content = weighted_tag.sub(r'\1\2', content)
            if weighted_captions:
                # re-apply changes
                content = content.replace(r'(', r'\(').replace(r')', r'\)').replace(r':', r'\:')
                if keep_tokens_weight > 1:
                    tags = [s.strip() for s in content.split(",")]
                    for i in range(min(keep_tokens, len(tags))):
                        tags[i] = f'({tags[i]}:{keep_tokens_weight})'
                    content = ", ".join(tags)
            with open(os.path.join(folder, txt), 'w') as f:
                f.write(content)


def create_config():
    global dataset_config_file, config_file, model_file

    if resume:
        resume_points = [f.path for f in os.scandir(output_folder) if f.is_dir()]
        resume_points.sort()
        last_resume_point = resume_points[-1] if resume_points else None
    else:
        last_resume_point = None

    if override_config_file:
        config_file = override_config_file
        print(f"\n⭕ Using custom config file {config_file}")
    else:
        config_dict = {
            "additional_network_arguments": {
                "unet_lr": unet_lr,
                "text_encoder_lr": text_encoder_lr,
                "network_dim": network_dim,
                "network_alpha": network_alpha,
                "network_module": network_module,
                "network_args": network_args,
                "network_train_unet_only": True if text_encoder_lr == 0 else None,
                "network_weights": continue_from_lora if continue_from_lora else None
            },
            "optimizer_arguments": {
                "learning_rate": unet_lr,
                "lr_scheduler": lr_scheduler,
                "lr_scheduler_num_cycles": lr_scheduler_num_cycles if lr_scheduler == "cosine_with_restarts" else None,
                "lr_scheduler_power": lr_scheduler_power if lr_scheduler == "polynomial" else None,
                "lr_warmup_steps": lr_warmup_steps if lr_scheduler != "constant" else None,
                "optimizer_type": optimizer,
                "optimizer_args": optimizer_args if optimizer_args else None,
            },
            "training_arguments": {
                "max_train_steps": max_train_steps,
                "max_train_epochs": max_train_epochs,
                "save_every_n_epochs": save_every_n_epochs,
                "save_last_n_epochs": keep_only_last_n_epochs,
                "train_batch_size": train_batch_size,
                "noise_offset": None,
                "clip_skip": 2,
                "min_snr_gamma": min_snr_gamma_value,
                "weighted_captions": weighted_captions,
                "seed": 42,
                "max_token_length": 225,
                "xformers": True,
                "lowram": COLAB,
                "max_data_loader_n_workers": 8,
                "persistent_data_loader_workers": True,
                "save_precision": "fp16",
                "mixed_precision": "fp16",
                "output_dir": output_folder,
                "logging_dir": log_folder,
                "output_name": project_name,
                "log_prefix": project_name,
                "save_state": save_state,
                "save_last_n_epochs_state": 1 if save_state else None,
                "resume": last_resume_point
            },
            "model_arguments": {
                "pretrained_model_name_or_path": model_file,
                "v2": custom_model_is_based_on_sd2,
                "v_parameterization": True if custom_model_is_based_on_sd2 else None,
            },
            "saving_arguments": {
                "save_model_as": "safetensors",
            },
            "dreambooth_arguments": {
                "prior_loss_weight": 1.0,
            },
            "dataset_arguments": {
                "cache_latents": True,
            },
        }

        for key in config_dict:
            if isinstance(config_dict[key], dict):
                config_dict[key] = {k: v for k, v in config_dict[key].items() if v is not None}

        with open(config_file, "w") as f:
            f.write(toml.dumps(config_dict))
        print(f"\n📄 Config saved to {config_file}")

    if override_dataset_config_file:
        dataset_config_file = override_dataset_config_file
        print(f"⭕ Using custom dataset config file {dataset_config_file}")
    else:
        dataset_config_dict = {
            "general": {
                "resolution": resolution,
                "shuffle_caption": shuffle_caption,
                "keep_tokens": keep_tokens,
                "flip_aug": flip_aug,
                "caption_extension": caption_extension,
                "enable_bucket": True,
                "bucket_reso_steps": 64,
                "bucket_no_upscale": False,
                "min_bucket_reso": 320 if resolution > 640 else 256,
                "max_bucket_reso": 1280 if resolution > 640 else 1024,
            },
            "datasets": toml.loads(custom_dataset)["datasets"] if custom_dataset else [
                {
                    "subsets": [
                        {
                            "num_repeats": num_repeats,
                            "image_dir": images_folder,
                            "class_tokens": None if caption_extension else project_name
                        }
                    ]
                }
            ]
        }

        for key in dataset_config_dict:
            if isinstance(dataset_config_dict[key], dict):
                dataset_config_dict[key] = {k: v for k, v in dataset_config_dict[key].items() if v is not None}

        with open(dataset_config_file, "w") as f:
            f.write(toml.dumps(dataset_config_dict))
        print(f"📄 Dataset config saved to {dataset_config_file}")


def download_model():
    global old_model_url, model_url, model_file
    real_model_url = model_url.strip()

    if real_model_url.lower().endswith((".ckpt", ".safetensors")):
        model_file = f"/content{real_model_url[real_model_url.rfind('/'):]}"
    else:
        model_file = "/content/downloaded_model.safetensors"
        if os.path.exists(model_file):
            !rm
            "{model_file}"

    if m := re.search(r"(?:https?://)?(?:www\.)?huggingface\.co/[^/]+/[^/]+/blob", model_url):
        real_model_url = real_model_url.replace("blob", "resolve")
    elif m := re.search(r"(?:https?://)?(?:www\.)?civitai\.com/models/([0-9]+)", model_url):
        real_model_url = f"https://civitai.com/api/download/models/{m.group(1)}"

    !aria2c
    "{real_model_url}" - -console - log - level = warn - c - s
    16 - x
    16 - k
    10
    M - d / -o
    "{model_file}"

    if model_file.lower().endswith(".safetensors"):
        from safetensors.torch import load_file as load_safetensors
        try:
            test = load_safetensors(model_file)
            del test
        except Exception as e:
            # if "HeaderTooLarge" in str(e):
            new_model_file = os.path.splitext(model_file)[0] + ".ckpt"
            !mv
            "{model_file}" "{new_model_file}"
            model_file = new_model_file
            print(f"Renamed model to {os.path.splitext(model_file)[0]}.ckpt")

    if model_file.lower().endswith(".ckpt"):
        from torch import load as load_ckpt
        try:
            test = load_ckpt(model_file)
            del test
        except Exception as e:
            return False

    return True


def main():
    global dependencies_installed

    if COLAB and not os.path.exists('/content/drive'):
        from google.colab import drive
        print("📂 Connecting to Google Drive...")
        drive.mount('/content/drive')

    for dir in (main_dir, deps_dir, repo_dir, log_folder, images_folder, output_folder, config_folder):
        os.makedirs(dir, exist_ok=True)

    if not validate_dataset():
        return

    if not dependencies_installed:
        print("\n🏭 Installing dependencies...\n")
        t0 = time()
        install_dependencies()
        t1 = time()
        dependencies_installed = True
        print(f"\n✅ Installation finished in {int(t1 - t0)} seconds.")
    else:
        print("\n✅ Dependencies already installed.")

    if old_model_url != model_url or not model_file or not os.path.exists(model_file):
        print("\n🔄 Downloading model...")
        if not download_model():
            print(
                "\n💥 Error: The model you selected is invalid or corrupted, or couldn't be downloaded. You can use a civitai or huggingface link, or any direct download link.")
            return
        print()
    else:
        print("\n🔄 Model already downloaded.\n")

    create_config()

    print("\n⭐ Starting trainer...\n")
    os.chdir(repo_dir)

    !accelerate
    launch - -config_file = {accelerate_config_file} - -num_cpu_threads_per_process = 1
    train_network.py - -dataset_config = {dataset_config_file} - -config_file = {config_file}

    if not get_ipython().__dict__['user_ns']['_exit_code']:
        display(Markdown(
            "### ✅ Done! [Go download your Lora(s) from Google Drive](https://drive.google.com/drive/my-drive)"))


main()
