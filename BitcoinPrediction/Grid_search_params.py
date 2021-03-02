from BitcoinPrediction.trainer import Trainer

trainer_params = dict(
    model_init=[RidgeClassifier()]
    sample_size=[1_000, 2000, 3000],
    train_fraction=[0.5, 0.7],
    features_size=[5, 60],
    horizon=[1, 5],
    data_start=["2020-10-1"],
    data_end=["2020-10-6"],
)

# hyper_params = dict(
#     random_forest=dict(
#         max_depth=[1, 2, 3],
#         with_mean=[True, False]
#     ),
#     linear_regression=dict(
#         features__distance__distancetransformer__distance_type=["euclidian", "manhattan"],
#         features__distance__standardscaler__with_mean=[True, False],
#         model__normalize=[True, False]
#     )
# )

trainer = Trainer()
models = trainer.train(trainer_params, hyper_params)
models