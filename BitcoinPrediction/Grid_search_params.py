from coin.trainer import Trainer

trainer_params = dict(
    sample_size=[1_000, 100_000, 200_000],
    shift_size=[5, 100],
    train_size=[2],
    horizon=[1_000],
    data_start=[1_000],
    data_end=[1_000],
)

hyper_params = dict(
    random_forest=dict(
        max_depth=[1, 2, 3],
        with_mean=[True, False]
    ),
    linear_regression=dict(
        features__distance__distancetransformer__distance_type=["euclidian", "manhattan"],
        features__distance__standardscaler__with_mean=[True, False],
        model__normalize=[True, False]
    )
)

trainer = Trainer()
models = trainer.train(trainer_params, hyper_params)
models