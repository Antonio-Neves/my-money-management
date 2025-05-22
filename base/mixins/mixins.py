class FilterUserConnected():
    """
    Mixin
    - Confirm user is authenticated
    - If authenticated filter user_connected
    """

    def get_queryset(self):

        # queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            return super().get_queryset().filter(user_conected=self.request.user)

        else:
            return super().get_queryset().filter(user_connected=None)
