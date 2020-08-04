from database import Setup

# from Common.server import Network

Setup().create_all_or_pass()

Setup().make_migrate()
