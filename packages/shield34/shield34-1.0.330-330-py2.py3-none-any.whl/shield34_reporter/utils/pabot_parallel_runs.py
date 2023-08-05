class PabotParallelRuns():

    pabotlib_intance = None
    def is_pabot_exists(self):
        try:
            from pabot import pabot
        except ImportError:
            from shield34_reporter.listeners.shield34_listener import Shield34Listener
            return False

        return True

    def is_pabotlib_exists(self):
        try:
            from pabot import pabotlib
        except ImportError:
            from shield34_reporter.listeners.shield34_listener import Shield34Listener
            return False
        from shield34_reporter.listeners.shield34_listener import Shield34Listener
        return True

    def __init__(self):
        if self.is_pabotlib_exists() and self.is_pabot_exists():
            from pabot import PabotLib
            try :
                self.pabotlib_intance = PabotLib()

            except Exception as e:
                pass

    def check_if_key_is_shared(self, key):
        if self.is_pabotlib_exists():
            try:
                key_value = self.pabotlib_intance.get_parallel_value_for_key(key)
                if key_value == '':
                    return False
                else:
                    return True
            except Exception as e:
                raise e

    def acquire_lock(self, key):
        if self.is_pabotlib_exists():
            try:
                self.pabotlib_intance.acquire_lock(key)

            except Exception as e:
                raise e

    def release_lock(self, key):
        if self.is_pabotlib_exists():
            try:
                self.pabotlib_intance.release_lock(key)
                from shield34_reporter.listeners.shield34_listener import Shield34Listener
            except Exception as e:
                raise e

    def set_shared_key(self, key, value):
        if self.is_pabotlib_exists():
            try:
                self.pabotlib_intance.set_parallel_value_for_key(key=key, value=value)
                from shield34_reporter.listeners.shield34_listener import Shield34Listener
            except Exception as e:
                raise e

    def get_shared_key(self, key):
        if self.is_pabotlib_exists():
            try:
                shared_key = self.pabotlib_intance.get_parallel_value_for_key(key=key)
                from shield34_reporter.listeners.shield34_listener import Shield34Listener
                return shared_key
            except Exception as e:
                raise e

    def get_existing_run(self):

        from shield34_reporter.model.contracts.run_contract import RunContract
        run_contract_id = self.get_shared_key("shield34_run_id")
        run_contract_index = self.get_shared_key("shield34_run_index")
        run_contract_start_timestamp = int(self.get_shared_key("shield34_run_start_timestamp"))
        run_contract_name = self.get_shared_key("shield34_run_name")
        return RunContract(run_name=run_contract_name, index=run_contract_index,
                           start_timestamp=run_contract_start_timestamp, id=run_contract_id)

    def set_run(self, run_contract):
        self.set_shared_key("shield34_run_id", run_contract.id)
        self.set_shared_key("shield34_run_index", run_contract.index)
        self.set_shared_key("shield34_run_start_timestamp", str(run_contract.startTimestamp))
        self.set_shared_key("shield34_run_name", run_contract.runName)