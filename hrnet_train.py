import sys


def train(batch_size, num_workers, start_epoch, epochs, version):

    from src.configs import cfg
    import src.models.gaze_hrnet as gaze_hrnet
    model = gaze_hrnet.get_gaze_net(cfg, is_train=True).cuda()
    # model = torch.load("./models/...")

    from torch.utils.data import DataLoader
    from src.datasources.unityeyes import UnityEyesDataset
    dataset_path = 'E:/Datasets/UnityEyes_Windows/480x640'
    # dataset_path = ''

    train_dataset = UnityEyesDataset(dataset_path, cfg, is_train=True, random_difficulty=True, generate_heatmaps=True)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=batch_size, num_workers=num_workers)

    val_dataset = UnityEyesDataset(dataset_path, cfg, is_train=False, random_difficulty=False, generate_heatmaps=True)
    val_dataloader = DataLoader(val_dataset, shuffle=False, batch_size=batch_size, num_workers=num_workers)

    from src.trainers.hrnet_trainer import HRNetTrainer
    trainer = HRNetTrainer(
        model=model,
        train_dataset=train_dataloader,
        val_dataset=val_dataloader,
        epochs=epochs,
        batch_size=16,
        initial_learning_rate=0.001,
        start_epoch=start_epoch,
        print_freq=500,
        version='v0.1',
        tensorboard_dir='./logs'
        )

    trainer.run()


if __name__ == "__main__":
    batch_size = eval(sys.argv[1])
    num_workers = eval(sys.argv[2])
    start_epoch = eval(sys.argv[3])
    epochs = eval(sys.argv[4])

    train(batch_size, num_workers, start_epoch, epochs, version=f'v0.1')
    