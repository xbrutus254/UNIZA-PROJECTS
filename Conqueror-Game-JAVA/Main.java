import java.util.Scanner;

/**
 * Write a description of class Pict here.
 * 
 * @author NightRain
 * @version 13-Nov-18
 */

public class Main {
    
    //private String totalName = "";
    public static void main(String[] args) {
        System.out.println("-----------------------SMBS----------------------");
        System.out.println("Welcome in Simulator of Ballistic Missile Strikes!");
        
        Scanner reader = new Scanner(System.in);  // Reading from System.in    
        System.out.println(">> Enter name: ");
        String name = reader.nextLine();
        
        System.out.println(">> Enter rank: ");
        System.out.println("1) General  <****>\n2) Colonel  <***>\n3)" 
                           +  " Major    <**>\n4) Lower");
        int rank = reader.nextInt();
        reader.nextLine();
        
        if (rank < 0 || 4 <= rank) {
            System.out.println(">> You are not allowed to use SMBS!");
            System.out.println(">> SMBS returned Exit!");
            return;
        }
        
        String s = "";
        if (rank == 1) {
            s = "General ";
            name = s.concat(name);
        } else if (rank == 2) {
            s = "Colonel ";
            name = s.concat(name);
        } else if (rank == 3) {
            s = "Major ";
            name = s.concat(name);
        }
        
        System.out.println(">> " + name + ", now we are prepare\n   to fire some missile!");
        System.out.println(">> Can we continue?");
        System.out.println(">> Type yes/no");
        String yesNo = reader.nextLine();
        
        if (yesNo.equals("no")) {
            System.out.println(">> SMBS returned Exit!");
            return;
        }
        
        System.out.println(">> Choose country:");
        System.out.println("1) Algeria\n2) German\n3)" 
                           +  " France\n4) Iran\n5) Kazakhstan\n6) Poland\n"
                           + "7) Saudi Arabia\n8) Slovakia");
                           
        int countryNum = reader.nextInt();
        reader.nextLine();
        
        
        if ( 0 < countryNum && countryNum <= 8) {
            /*
             *  Create canvas
             */
            new Canvas(countryNum);
 
        } else {
            System.out.println(">> Invalid choice of country!");
            System.out.println(">> SMBS returned Exit!");
            return;
        } 
        System.out.println("------------MESSAGES---------------");
        
    }  
    

    
}
