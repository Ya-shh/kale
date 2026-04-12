import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import {
  ABCWidgetFactory,
  DocumentRegistry,
  DocumentWidget
} from '@jupyterlab/docregistry';

import { WorkflowPanel } from './WorkflowWidget';

const FILE_TYPE = 'demo-workflow';
const FACTORY = 'WorkflowEditor';

class WorkflowFactory extends ABCWidgetFactory<
  DocumentWidget<WorkflowPanel>,
  DocumentRegistry.IModel
> {
  protected createNewWidget(
    context: DocumentRegistry.Context
  ): DocumentWidget<WorkflowPanel> {
    const content = new WorkflowPanel(context);
    return new DocumentWidget({ content, context });
  }
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'minimal-workflow-widget:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    app.docRegistry.addFileType({
      name: FILE_TYPE,
      displayName: 'Kale Workflow (demo)',
      extensions: ['.demo-workflow'],
      mimeTypes: ['application/json'],
      contentType: 'file',
      fileFormat: 'text'
    });

    app.docRegistry.addWidgetFactory(
      new WorkflowFactory({
        name: FACTORY,
        fileTypes: [FILE_TYPE],
        defaultFor: [FILE_TYPE]
      })
    );

    console.log('minimal-workflow-widget activated');
  }
};

export default plugin;
