'''
Preprocessor for Foliant documentation authoring tool.
Renders ImagineUI wireframes and inserts them into documents.

Uses Node.js, headless Chrome, Puppeteer and ImagineUI.
'''

import re
from pathlib import Path
from hashlib import md5
from subprocess import run, PIPE, STDOUT, CalledProcessError
from time import sleep
from typing import Dict
OptionValue = int or float or bool or str

from foliant.utils import output
from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'version': 'latest',
        'cache_dir': Path('.imagineuicache'),
    }

    tags = 'imagineui',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cache_dir_path = (self.project_path / self.options['cache_dir']).resolve()

        self.logger = self.logger.getChild('imagineui')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    # def _process_imagineui(self, options: Dict[str, OptionValue]) -> str:
    #     img_url = self._img_urls[options.get('url', '')]
    #
    #     if not img_url.startswith('https://cdn.imagineui.io/'):
    #         return ''
    #
    #     img_hash = f'{md5(img_url.encode()).hexdigest()}'
    #
    #     original_img_path = (self._cache_dir_path / f'original_{img_hash}.png').resolve()
    #
    #     self.logger.debug(f'Original image path: {original_img_path}')
    #
    #     if not original_img_path.exists():
    #         self.logger.debug('Original image not found in cache')
    #
    #         try:
    #             self.logger.debug(f'Downloading original image: {img_url}')
    #
    #             command = (
    #                 f'{self.options["wget_path"]} ' +
    #                 f'-O {original_img_path} ' +
    #                 f'{img_url}'
    #             )
    #
    #             run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)
    #
    #         except CalledProcessError as exception:
    #             self.logger.error(str(exception))
    #
    #             raise RuntimeError(f'Failed: {exception.output.decode()}')
    #
    #     resized_img_width = options.get('width', self.options['image_width'])
    #
    #     self.logger.debug(f'Resized image width: {resized_img_width}')
    #
    #     resized_img_path = (
    #         self._cache_dir_path /
    #         f'resized_{resized_img_width}_{img_hash}.png'
    #     ).resolve()
    #
    #     self.logger.debug(f'Resized image path: {resized_img_path}')
    #
    #     if not resized_img_path.exists():
    #         self.logger.debug('Resized image not found in cache')
    #
    #         try:
    #             self.logger.debug(f'Resizing original image, width: {self.options["image_width"]}')
    #
    #             command = (
    #                 f'{self.options["convert_path"]} ' +
    #                 f'{original_img_path} ' +
    #                 f'-resize {resized_img_width} ' +
    #                 f'{resized_img_path}'
    #             )
    #
    #             run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)
    #
    #         except CalledProcessError as exception:
    #             self.logger.error(str(exception))
    #
    #             raise RuntimeError(f'Failed: {exception.output.decode()}')
    #
    #     resized_img_ref = f'![{options.get("caption", "")}]({resized_img_path})'
    #
    #     return resized_img_ref
    #
    # def process_imagineui(self, markdown_content: str) -> str:
    #     def _sub(design_definition) -> str:
    #         return self._process_imagineui(self.get_options(design_definition.group('options')))
    #
    #     return self.pattern.sub(_sub, markdown_content)

    def apply(self):
        self.logger.info('Applying preprocessor')

        wireframe_files = []

        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                markdown_content = markdown_file.read()

            wireframe_definitions = re.finditer(self.pattern, markdown_content)

            for wireframe_definition in wireframe_definitions:
                self.logger.debug(wireframe_definition)
                # wireframe_file = self.get_options(wireframe_definition.group('options')).get('url', '')
                #
                # if wireframe_file not in wireframe_files:
                #     # TODO: Write a file {self._cache_dir_path}
                #     wireframe_files.append(wireframe_file)

        self.logger.debug(f'Design URLs: {wireframe_files}')

        if wireframe_files:
            self._cache_dir_path.mkdir(parents=True, exist_ok=True)

            output('Trying to run Puppeteer-based script', self.quiet)

            input_param = " \n".join(map(lambda x: f'--input=' + x, wireframe_files))

            command = (
                f'npx imagineui-cli@{self.options["version"]} ' +
                f'--outputDir={self._cache_dir_path} ' +
                input_param
            )

            self.logger.debug(f'Running ImagineUI through NPX')

            command_output = run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

            if command_output.stdout:
                output(command_output.stdout.decode('utf8', errors='ignore'), self.quiet)


            # for line in img_urls_file:
            #     (wireframe_file, img_url) = line.split()
            #
            #     self._img_urls[wireframe_file] = img_url
            #
            #     if not img_url.startswith('https://cdn.imagineui.io/'):
            #         warning_message = f'Invalid image URL for the design page {wireframe_file}: {img_url}'
            #
            #         if img_url == 'NOT_FOUND':
            #             warning_message = f'Design {wireframe_file} not found'
            #
            #         self.logger.warning(warning_message)
            #
            #         output(warning_message, self.quiet)
            #
            #         continue
            #
            # for markdown_file_path in self.working_dir.rglob('*.md'):
            #     with open(markdown_file_path, encoding='utf8') as markdown_file:
            #         markdown_content = markdown_file.read()
            #
            #     processed_content = self.process_imagineui(markdown_content)
            #
            #     if processed_content:
            #         with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
            #             markdown_file.write(processed_content)

        self.logger.info('Preprocessor applied')
