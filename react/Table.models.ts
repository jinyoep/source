import React, {    
    CSSProperties,    
} from 'react';
import { ColumnType } from 'antd/lib/table';
import { FormInstance } from 'antd/lib/form';

export interface ETableColEditorProps {
    type?: 'select' | 'datetime' | 'string' | 'checkbox' | 'number' | 'date' | 'time';
    required?: boolean;
    validator?: (...arg: any[]) => void;
    options?: any[];
    format?: string;
    max?: number;
    min?: number;
    regex?: RegExp;
    component?: ()=> React.ReactElement;
  }

export interface ETableColProps<T> extends ColumnType<T> {
    editable?: (...arg: any[]) => boolean | true | false;
    editor?: ETableColEditorProps;
    children?: ETableColProps<any>[];
  }

export interface EditableContextProps {
    rowKey?: string;
    changedData?: any[];
    filter?: any;
    filterVisible?: boolean;
    setFilter?: (...args: any[]) => void;
    selectedRowKeys?: string[];
    showSelector?: boolean;
    columns?: ETableColProps<any>[];
    setColumns?: (cols: ETableColProps<any>[]) => void;
    handleTableChange?: (p?: any, f?: any, s?: any) => void;
    expandedRowRender?: (record) => React.ReactNode;
  }

export interface ResizeableCellProps {
    index: number;
    width?: number;
  }

export  interface EditableCellProps {
    editor?: ETableColEditorProps;
    editing?: boolean;
    dataIndex?: string | string[];
    title?: string;
    record?: any;
    index?: number;
  }

  export interface ETableProps {
    name?: string;
    bordered?: boolean;
    lang?: 'ko' | 'en' | 'pt_br';
    rowKey?: string;
    title?: string;
    style?: CSSProperties;
    newRowKeyPrefix?: string;
    cols?: ETableColProps<any>[];
    allCols?: ETableColProps<any>[];
    data?: any[];
    orgdata?: any[];
    changedData?: any[];
    loading?: boolean;
    selectedRowData?: any[];
    currentPage?: number;
    pageSize?: number;
    total?: number;
    scroll?: any;
    multiSelect?: boolean;
    showHeader?: boolean;
    showFooter?: boolean;
    showToolbar?: boolean;
    showAddBtn?: boolean;
    showOpBtn?: boolean;
    showSelectRecord?: boolean;
    showSelector?: boolean;
    showTopPager?: boolean;
    showBottomPager?: boolean;
    showExpandBtn?: boolean;
    showSearchInput?: boolean;
    showDownload?: boolean;
    buttons?: React.ReactElement,
    canEdit?: (...args: any[]) => boolean;
    canRemove?: (...args: any[]) => boolean;
    beforeEdit?: (...args: any[]) => any;
    afterEdit?: (...args: any[]) => any;
    onAdd?: (...args: any[]) => any;
    onFetch?: (...args: any[]) => void;
    onChangedDataUpdate?: (...args: any[]) => void;
    onChangedSelectedDataUpdate?: (...args: any[]) => void;
    onDownload?: (...args: any[]) => any;
    onSelectRow?: (...args: any[]) => void;
    onAddRow?: (...args: any[]) => void;
    expandedRowRender?: (record) => React.ReactNode;
    expandedFirstRow?: boolean;
    editOnSelected?: boolean;
    onExpandedRow?: (...args: any[]) => void;
    parentForm?: FormInstance;
  }