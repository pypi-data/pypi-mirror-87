import simplify.auth
import tqdm
import os
import simplify.drive
import shutil
from googleapiclient.http import MediaIoBaseDownload
import simplify.templates
from typing import Union
import git


class Builder:
    def __init__(self, drive_str: str, template_dir: str):
        self.drive_str = drive_str
        self.creds = simplify.auth.load_creds()
        self.drive = simplify.drive.Drive(drive_str, self.creds)
        self.templator = simplify.templates.Templates(template_dir)

        self.folders = self.drive.folders()
        self.file_tree = self.construct_folder_tree()

    @staticmethod
    def path_join(folder: simplify.typedefs.FolderType, prefix: str = "./build/"):
        return prefix + "/".join(folder.path) + "/"

    def construct_folder_tree(
        self, path: list = [""], start_folder: str = None
    ) -> list:
        """
        Recursively builds a folder tree.

        Note: This could be a contraction algo, but why bother?
        """
        if start_folder:
            pass
        elif self.folders:
            start_folder = self.drive_str
        else:
            return []

        level_folders = []  # all the folders within this level
        for each_folder in self.folders:
            if start_folder == each_folder.parents:
                each_folder.path = path + [each_folder.name]
                level_folders.append(
                    (
                        each_folder,
                        self.construct_folder_tree(
                            start_folder=each_folder.id, path=each_folder.path
                        ),
                    )
                )

        return level_folders

    def find_folder(
        self, folder: str
    ) -> Union[simplify.typedefs.DocType, simplify.typedefs.Drive]:
        if folder == self.drive_str:
            return simplify.typedefs.Drive()

        for each_folder in self.folders:
            if each_folder.id == folder:
                return each_folder

    def fetch_commit(self) -> str:
        """
        Fetches latest commit hash of repo.
        """
        repo = git.Repo(search_parent_directories=True)
        commit = repo.head.object.hexsha
        return commit[:6]

    def build(self, visual=True):
        """
        Loops and builds static website.
        """
        for each_doc in self.drive.docs(public=True):
            path = self.path_join(
                self.find_folder(each_doc.parents),
                prefix=f"./build/{self.fetch_commit()}",
            )

            if not os.path.exists("./build"):
                os.mkdir("./build")

            if not os.path.exists(path):
                os.mkdir(path)

            with open(path + each_doc.pointer.lower() + ".html", "w") as f:
                f.write(self.render(each_doc))

        for each_file in self.drive.media(public=True):
            path = self.path_join(
                self.find_folder(each_file.parents),
                prefix=f"./build/{self.fetch_commit()}",
            )
            if not os.path.exists(path):
                os.mkdir(path)

            with open(path + each_file.pointer.lower(), "wb") as f:
                file_handler = self.drive.service.files().get_media(fileId=each_file.id)
                downloader = MediaIoBaseDownload(f, file_handler)  # from google's docs

                if visual:
                    pbar = tqdm.tqdm(total=100)

                done = False
                while done is False:
                    status, done = downloader.next_chunk()

                    if visual:
                        pbar.update(int(status.progress()) * 100)

                if visual:
                    pbar.close()

        shutil.rmtree("./build/latest", ignore_errors=True)
        shutil.copytree(f"./build/{self.fetch_commit()}", "./build/latest")

    def render(self, doc, template="example.html"):
        document = simplify.docs.Docs(doc, self.creds)
        return document.render(self.templator.get("example.html"))
