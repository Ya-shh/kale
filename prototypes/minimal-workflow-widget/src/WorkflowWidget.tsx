import { ReactWidget } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import * as React from 'react';
import ReactFlow, {
  Background,
  Controls,
  Edge,
  MiniMap,
  Node
} from 'reactflow';

import 'reactflow/dist/style.css';

const initialNodes: Node[] = [
  {
    id: 'data_prep',
    position: { x: 40, y: 80 },
    data: { label: 'data_prep.ipynb\n→ Dataset' },
    style: { padding: 10, border: '1px solid #2b8a3e', borderRadius: 6 }
  },
  {
    id: 'train',
    position: { x: 320, y: 80 },
    data: { label: 'train.ipynb\nDataset → Model' },
    style: { padding: 10, border: '1px solid #1971c2', borderRadius: 6 }
  },
  {
    id: 'evaluate',
    position: { x: 600, y: 80 },
    data: { label: 'evaluate.ipynb\nModel → Metrics' },
    style: { padding: 10, border: '1px solid #c92a2a', borderRadius: 6 }
  }
];

const initialEdges: Edge[] = [
  { id: 'e1', source: 'data_prep', target: 'train', label: 'Dataset', animated: true },
  { id: 'e2', source: 'train', target: 'evaluate', label: 'Model', animated: true }
];

function Canvas(): JSX.Element {
  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ReactFlow nodes={initialNodes} edges={initialEdges} fitView>
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}

export class WorkflowPanel extends ReactWidget {
  constructor(private context: DocumentRegistry.Context) {
    super();
    this.addClass('kale-workflow-panel');
    this.title.label = context.path.split('/').pop() ?? 'Workflow';
  }

  protected render(): JSX.Element {
    return <Canvas />;
  }
}
