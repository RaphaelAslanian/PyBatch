class ARNObject:

    def __init__(
            self,
            name: str,
            resource: str,
            account: str = "446570804799",
            region: str = "eu-west-1",
            service: str = "batch",
            partition: str = "aws"
    ):
        self.arn = "arn:" \
                   + partition + ":" \
                   + service + ":" \
                   + region + ":" \
                   + account + ":" \
                   + resource
        self.name = name
