public class Rectangle {
    
    class Point {
        int x, y;

        Point() {
            x = y = 0;
        }
        
        Point(int x0, int y0) {
            x = x0;
            y = y0;
        }

        public String toString() {
            return "(" + x + "," + y + ")";
        }
    }

    Point bottomLeft;
    Point topRight; 

    Rectangle(int x1, int y1, int x2, int y2){
        bottomLeft = new Point (x1,y1);
        topRight = new Point(x2,y2);
    }
    
    Rectangle(Point p1, Point p2){
        bottomLeft = p1;
        topRight = p2;
    }

    public int area(){
        int comprimento = topRight.x - bottomLeft.x;
        int largura = topRight.y - bottomLeft.y;
        return comprimento * largura;
    }

    public int perimeter(){
        int comprimento = topRight.x - bottomLeft.x;
        int largura = topRight.y - bottomLeft.y;
        return comprimento * 2 + largura * 2; 
    }

    public boolean pointInside(Point p){
        int x = p.x;
        int y = p.y;

        if ( x <= topRight.x && x >= bottomLeft.x && y <= topRight.y && y >= bottomLeft.y ){
            return true;
        } else {
            return false;
        }
    }

    public boolean rectangleInside(Rectangle r){
        return (r.bottomLeft.x >= this.bottomLeft.x &&
                r.topRight.x   <= this.topRight.x   &&
                r.bottomLeft.y >= this.bottomLeft.y &&
                r.topRight.y   <= this.topRight.y);
    }
}
