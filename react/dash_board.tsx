import React, { useEffect, useState, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../modules';
import { getDashBardProfileAsync } from '../modules/dashboard';
import ReactExport from "react-export-excel";
import moment from 'moment';
import styled from 'styled-components';
import './dash_board.css';

import { Button, Table, Layout, Row, Col, Tabs, DatePicker, Input, message } from 'antd';
import 'antd/dist/antd.css';
import { render } from '@testing-library/react';

import TableComponet from "../Components/Table.Components";

function Dash_board() {

  const { Content } = Layout;
  const { TabPane } = Tabs;
  const selRow = useRef();

  const dateFormat = 'YYYY-MM-DD';

  const ButtonContainer = styled.div`
    .ant-btn-primary {
      background-color: #757575;
      border-color:  #757575;
    }
  `;

  const ExcelFile = ReactExport.ExcelFile;
  const ExcelSheet = ReactExport.ExcelFile.ExcelSheet;
  //const ExcelColumn = ReactExport.ExcelFile.ExcelColumn;

  const { data, loading, error } = useSelector((state: RootState) => state.dashboard.dashboardProfile);
  const dispatch = useDispatch();

  const [tdata, setTdata] = useState([]);
  const [tdata3, setTdata3] = useState([]);

  
  const [originalData, setOriginalData] = useState([]);

  const [tkey, setTkey] = useState([]);

  const [filterData, setFilterData] = useState([]); 
  const [multiDataSet2, setMultiDataSet2] = useState([]);

  const [changedData,setChangedData] = useState([]);
  const [onAddRowFun,setOnAddRowFun] = useState([]);

  const [selectedRowData,setSelectedRowData] = useState({});

  const [tableLoading, setTableLoading] = useState(false);

  

  const [rowClick, setRowClick] = useState({seq:''});

  
  

  const test = (user:string) => {
    console.log("#user :" + user)
    setTableLoading(true);
    dispatch(getDashBardProfileAsync.request(user));
   
       
  }


  const search = (searchInput:string) => {    
    console.log("PASS", { searchInput });

    let filteredData = originalData.filter(value => {
      return (
        value.id.toLowerCase().includes(searchInput.toLowerCase()) ||
        value.name.toLowerCase().includes(searchInput.toLowerCase()) ||
        value.etc
          .toString()
          .toLowerCase()
          .includes(searchInput.toLowerCase())
      );
    });

    console.log("filterTable:", filteredData);

    setTdata(filteredData);
    //setState({ data: filteredData });
    
  };

  const columns = [
    {
      title: 'seq',
      dataIndex: 'seq',
      render(text, record) {
        return {
        	props: {
            style: { background: '#eee' },
          },
        	children: <div>{text}</div>,
        };
      },
    },
    {
      title: 'id',
      dataIndex: 'id',  
      editable: true,
      
      
    },
    {
      title: 'name',
      dataIndex: 'name', 
      editable: true,
      
      
    },
    {
      title: 'etc',
      dataIndex: 'etc',  
      editable: true,
      
        
    },    
  ];

  const warning = () => {
    message.warning('조회 부터 하세요.');
  };

  const operations = (
    data === null ? <Button onClick={warning}>Excel</Button> : 
    <ExcelFile element={<Button>Excel</Button>} filename="TEST">
      <ExcelSheet dataSet={multiDataSet2} name="Sheet1"/>
    </ExcelFile>
  );
   
  const multiDataSet = [
    {
      columns: ["seq", "id", "name", "etc"],
      data: []
    },
  ];

  
  

  useEffect(() => {
        console.log('=== useEffect ===');

        
        if(data !== null){
          const j = Object.values(data);
        
          let tdata2 = [];
          let tkey2 = [];
          let test = [
            {
              columns: ["seq", "id", "name", "etc"],
              data: []
            }
          ];
          j && j.map((journal, index) => {          
            if(journal !== null){           
              let data1 = [{value: journal.seq.toString()},{value: journal.id},{value: journal.name},{value: journal.etc}];                 
              multiDataSet[0].data.push(data1)
              test[0].data.push(data1)              
              tdata2.push({seq: journal.seq, id: journal.id, name: journal.name, etc: journal.etc});
              tkey2.push(index);
              return  ( console.log("#t2 :" + journal.seq + journal.id + journal.name + journal.etc) )              
            } else {
              return  ( console.log("#t3 :" + journal ) )
            }          
            
            
            
          })

          selectedRow({seq:j[0].seq, id:j[0].id, name:j[0].name, etc:j[0].etc});

          setMultiDataSet2(test);

          setTdata(tdata2);          
          setTdata3(tdata2);
          setOriginalData(tdata2);
          setTkey(tkey2);

          setTableLoading(false);
        }

        console.log("multiDataSet:", multiDataSet)

        console.log("data:",data)
        console.log("#tdata:",tdata)      
             
        
        console.log("#loading :" + loading);
        console.log("#error :" + error);
  },[data, rowClick, tableLoading, loading, error]);

  



  function changefun(rs){
    console.log("################## parent chagefun : ", rs);    
    let chk2 = rs.map(item =>{ return item.isUpdate; });
    let chk1 = rs.map(item =>{ return item.isDelete; });
    let seq = rs.map(item =>{ return item.seq; });
    console.log('# changefun_chk1 : ', chk1) ;
    console.log('# changefun_seq : ', seq) ;

    tdata.map(item =>{ console.log('######## tdata.item : ', item); });

    if(chk1){      
      const fe = tdata.filter(item => parseInt(item.seq) !== parseInt(seq));
      console.log('# changefun_tdata : ', fe);
      setTdata(fe);
    }
       
    if(chk2){
      setChangedData(rs);
    }

  }

  function changeSelect(rs, rs2){
    setTdata(rs);
    setOriginalData(rs2);
  }

  const childRef = useRef<any>();



  function addRow(){
    //let newData = [];
    //newData.push({sep:5, id:'TEST', name:'new data', etc:'module'});
    //setChangedData(newData);
    //setOnAddObj({sep:5, id:'TEST', name:'new data', etc:'module'});
    //child.current.handleAdd();
    //childRef.current.sayHi();
    

 
    
  }

  function selectedRow(e){
    console.log('#### selectedRow : ', e);
    setSelectedRowData(e);
  }

  

  const onClickRow = (record) => {
    console.log('#onClickRow : ', record);
    return {
      onClick: () => {
        setRowClick({seq:record.seq });
      },
    };
  }
  const setRowClassName = (record) => {
    console.log('#setRowClassName : ', record);
    return record.seq === rowClick.seq ? 'clickRowStyle' : '';
  }


  
  
  console.log("#tdata2:",tdata)
  return (
    <div>
      <Layout>      
        <Content>             
          <Row>
            <DatePicker defaultValue={moment(new Date(), dateFormat)} format={dateFormat} />
            <Button type="primary" onClick={() => test("TEST") } >
              조회
            </Button>  
          </Row>
          <Row>
              <Input.Search
              style={{ border: "3px solid red", margin: "0 0 10px 0" }}
              placeholder="Search by..."
              enterButton
              onSearch={search}
            />
          </Row>  
          <Row>
            <Tabs type="card" tabBarExtraContent={operations}>
              <TabPane tab="Tab 1" key="1">
                <Table columns={columns} dataSource={tdata} rowKey="seq" 
                  onRow={onClickRow} 
                  rowClassName="table-hover"                  
                />  
              </TabPane>
              <TabPane tab="Tab 2" key="2">
              <Table columns={columns} dataSource={tdata3} rowKey="seq" />
              </TabPane>
              <TabPane tab="Tab 3" key="3">
                Content of Tab Pane 3
              </TabPane>
            </Tabs>
            
          </Row>
          <Row>
            <ButtonContainer>
            <Button type="primary" onClick={() => addRow() } >
              추가
            </Button> 
            </ButtonContainer>
            <Button type="primary" onClick={() => addRow() } style={{ background: "red", borderColor: "yellow" }} >
              추가2
            </Button> 
          </Row>
          <Row>
            <TableComponet 
              cols={columns}              
              data={tdata}   
              orgdata={originalData} 
              rowKey={'seq'}//{(recode, index) => index}              
              total={tdata.length} 
              bordered={true}      
              showSelectRecord={true}    
              showToolbar={true}     
              showAddBtn={true}  
              showTopPager={true}   
              showDownload={true}
              loading={tableLoading}
              showExpandBtn={true}  
              showSearchInput={true}   
              scroll={{x:800}}    
              changedData={changedData}               
              onChangedDataUpdate={(rs) => changefun(rs)}    
              onChangedSelectedDataUpdate={(rs, rs2) => changeSelect(rs, rs2)}
              selectedRow={selectedRowData}                             
              //style={{backgroundColor: '#d9d9d9'}}
              //ref={childRef }
              onSelectRow={(e) => selectedRow(e)}
              
            /> 
          </Row>
        </Content>      
      </Layout>
         
    </div>
  );
}

export default Dash_board;

