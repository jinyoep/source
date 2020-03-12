package csv_data_unpivot;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class readCsv {
	public static void main(String[] args) {

		 BufferedWriter bufWriter = null;
		 try{
			 bufWriter = Files.newBufferedWriter(Paths.get("C:\\Users\\zero\\Documents\\unpivot.csv"),StandardCharsets.UTF_8, StandardOpenOption.APPEND);
	
			// csv���� �б�
			List<List<String>> allData = readCSV();

			
			
			  for(List<String> newLine : allData){ 
				  List<String> list = newLine; 
				  int index = 0;
				  for(String data : list){ 
					  //System.out.println("data : " + data); 
					  bufWriter.write(data);
					  if(index < list.size()-1) {
						  bufWriter.write(",");
					  }
					   
					  index++;
				  } //�߰��ϱ� //bufWriter.write("�ּ�"); //�����ڵ��߰�
				  bufWriter.newLine(); 
			  }
		 }catch(FileNotFoundException e){ e.printStackTrace();
		  }catch(IOException e){ e.printStackTrace(); }finally{ try{ if(bufWriter !=
		  null){ bufWriter.close(); } }catch(IOException e){ e.printStackTrace(); } }
		  
		 

	}

	public static List<List<String>> readCSV() {
		// ��ȯ�� ����Ʈ
		List<List<String>> ret = new ArrayList<List<String>>();
		List<List<String>> ret2 = new ArrayList<List<String>>();
		BufferedReader br = null;

		try {
			//Charset charset_1 = Charset.forName("UTF-8");
			br = Files.newBufferedReader(Paths.get("C:\\Users\\zero\\Documents\\test.csv"), Charset.forName("UTF-8"));
			// Charset.forName("UTF-8");
			String line = "";

			while ((line = br.readLine()) != null) {
				// CSV 1���� �����ϴ� ����Ʈ
				List<String> tmpList = new ArrayList<String>();
				String array[] = line.split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)", -1);
				
				if(array.length > 0) {
					if(!array[0].equals("")) {
						// �迭���� ����Ʈ ��ȯ
						tmpList = Arrays.asList(array);
						// System.out.println(tmpList);
						ret.add(tmpList);				
					}				
				}				
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (br != null) {
					br.close();
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

		List<String> indexList = new ArrayList<String>();
		indexList = ret.get(0);

		int fixNo = 0; // master ��ġ
		int indexTotal = 0; // ��ü column ��

		indexTotal = indexList.size();

		for (int i = 0; i < indexList.size(); i++) {
			System.out.println(indexList.get(i));
			if (indexList.get(i).equals("master")) {
				fixNo = i;
			}
		}

		System.out.println("fixNo : " + fixNo);
		System.out.println("indexTotal : " + indexTotal);

		
//		  for(List<String> newLine : ret){ List<String> list = newLine; for(String data
//		  : list){ System.out.println("data : " + data); }
//		  
//		  
//		  }
		 

		List<String> tempList = new ArrayList<String>();
		List<String> tmpList = new ArrayList<String>();
		
		for (int i = 1; i < ret.size(); i++) {
			
			tempList = ret.get(i);
			String array[] = null;
			
			for(int c=0; c<(indexTotal-(fixNo + 1)) ; c++) {
				array = new String[fixNo + 3];
				for (int j = 0; j < tempList.size(); j++) {					
					if (j < fixNo + 1) {
						array[j] =  tempList.get(j);
					} else if(j == (fixNo + 1)) {
						array[j] =  indexList.get(fixNo + 1 + c);
					} else if(j == (fixNo + 2)) {
						array[j] =  tempList.get(fixNo + 1 + c);
					}
				}
				tmpList = Arrays.asList(array);
				ret2.add(tmpList);
				System.out.println(tmpList);
				
			}
			

		}

		//ret2.add(tmpList);
		
		System.out.println("ret2.size : " + ret2.size());

		return ret2;
		
		

	}

}
