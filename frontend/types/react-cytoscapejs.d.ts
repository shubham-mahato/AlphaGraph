/* eslint-disable @typescript-eslint/no-explicit-any */
declare module 'react-cytoscapejs' {
  import { Component, CSSProperties } from 'react';
  import cytoscape, { ElementDefinition, Stylesheet, LayoutOptions } from 'cytoscape';

  interface CytoscapeComponentProps {
    elements: ElementDefinition[];
    style?: CSSProperties;
    stylesheet?: Stylesheet[] | any; 
    layout?: LayoutOptions | any;
    cy?: (cy: cytoscape.Core) => void;
    className?: string;
    id?: string;
    [key: string]: any; 
  }

  export default class CytoscapeComponent extends Component<CytoscapeComponentProps> {}
}