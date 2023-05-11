table 50000 "Retention Policy Plus CCL"
{
    Caption = 'Retention Policy Plus';
    DataClassification = SystemMetadata;
    DrillDownPageId = "Retention Policies Plus CCL";
    LookupPageId = "Retention Policies Plus CCL";

    fields
    {
        field(1; "Table No."; Integer)
        {
            Caption = 'Table No.';
            TableRelation = AllObj."Object ID" where("Object Type" = const(Table));
        }
        field(2; Active; Boolean)
        {
            Caption = 'Active';
        }
        field(3; "Date Formula"; DateFormula)
        {
            Caption = 'Date Formula';

            trigger OnValidate()
            var
                validMsg: Label 'New formula accepted.\The cutoff point for %1 is %2.', Comment = '%1: Work date. %2: Result of CalcFormula using WorkDate.';
            begin
                Message(validMsg, System.WorkDate(), GetExpirationDate());
            end;
        }
        field(4; "Table Caption"; Text[249])
        {
            CalcFormula = lookup(AllObjWithCaption."Object Caption" where("Object Type" = const(Table), "Object ID" = field("Table No.")));
            Caption = 'Table Name';
            Editable = false;
            FieldClass = FlowField;
        }
    }
    keys
    {
        key(PK; "Table No.")
        {
            Clustered = true;
        }
        key(Active; Active, "Table No.") { }
    }

    fieldgroups
    {
        fieldgroup(Brick; "Table Caption", Active, "Date Formula") { }
        fieldgroup(DropDown; "Table Caption", Active, "Date Formula") { }
    }

    procedure GetExpirationDate(): Date
    begin
        exit(GetExpirationDate(WorkDate()));
    end;

    procedure GetExpirationDate(daInput: Date): Date
    var
        invertTok: Label '<-%1>', Locked = true;
    begin
        exit(CalcDate(StrSubstNo(invertTok, Rec."Date Formula"), daInput));
    end;
}
