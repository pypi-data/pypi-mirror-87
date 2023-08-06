import os

from matplotlib import pyplot


class ReportFigure:
    def __init__(self, img_path=None, title='', description='', tag=''):
        self.img_path = img_path
        self.title = title.replace(' ', '_')
        self.description = description
        self.tag = tag

    def __str__(self):
        return f'ReportFigure(\n\ttitle: {self.title},\n\tdescription: {self.description},\n\ttag: {self.tag}\n)'

    def __repr__(self):
        return f'ReportFigure(title: {self.title}, description: {self.description}, tag: {self.tag})'

    @staticmethod
    def of(name: str, report_directory: str, plot: pyplot):
        report_figure = ReportFigure()
        fig_rel_path = os.path.join('figures', f'{name}.png')
        fig_path = os.path.join(report_directory, fig_rel_path)

        plot.savefig(fig_path)
        plot.close()
        report_figure.img_path = fig_rel_path
        report_figure.title = name

        return report_figure
